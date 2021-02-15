require 'yaml'
require 'vagrant/errors'
require 'vagrant/ui'
require 'vagrant/util/downloader'
require 'vagrant/util/subprocess'

# Require Vagrant 2.0+.
Vagrant.require_version '>= 2.0.0'

# Setting up globals from YAML configuration file.
settings = YAML::load_file('docker-compose.yml')
vagrant_settings = settings.fetch('x-vagrant', {})
$images = vagrant_settings.fetch('images', {})
$project = 'geoint-deps'
$rpms = vagrant_settings.fetch('rpms', {})
$pg_version = settings.fetch('x-versions')['postgres']
$pg_dotless = $pg_version.gsub('.', '')

# Special workaround to have the `rpmbuild` UID and GID to match that of
# the user invoking Vagrant, which simplifies file permissions for host
# volume mounts.  Setting the `RPMBUILD_UID_MATCH` variable to a value
# other than '1' forces the UID/GID in the configuration file to be honored.
if ENV.fetch('RPMBUILD_UID_MATCH', '1') == '1'
  $images['base']['rpmbuild']['args']['rpmbuild_uid'] = Process.uid
  $images['base']['rpmbuild']['args']['rpmbuild_gid'] = Process.gid
end

## Functions used by Vagrant containers.

def build_requirements(spec_file)
  required_packages = []
  File.open(spec_file).read.each_line do |line|
    if line.start_with?('BuildRequires:')
      requirement = line.split[1]
      requirement = requirement.gsub('%{pg_dotless}', $pg_dotless)
      build_requirements << requirement
    end
  end
  return required_packages
end

def collect_rpms(filters)
  collected = {}
  filters.each do |filter|
    $rpms.each do |name, options|
      if (name == filter or
          options.fetch('image', nil) == filter)
        collected[name] = options
      end
    end
  end
  return collected
end


def shared_folders(container, name, options, rpmbuild: false)
  container.vm.synced_folder '.', '/vagrant', disabled: true

  if options.fetch('rpmbuild', rpmbuild)
    # Container needs to be able to write RPMs via bind mounts.
    container.vm.synced_folder 'RPMS', '/rpmbuild/RPMS'
    container.vm.synced_folder 'SPECS', '/rpmbuild/SPECS'
    container.vm.synced_folder 'SOURCES', '/rpmbuild/SOURCES'
    container.vm.synced_folder 'scripts', '/rpmbuild/scripts'
  end
end


def build_container(config, name, options)
  config.vm.define name do |container|
    shared_folders(container, name, options)

    container.vm.provider :docker do |d|
      # On the containers we're building don't actually run anything.
      d.build_dir = options.fetch('build_dir', '.')
      d.cmd = options.fetch('cmd', [])

      # Start build arguments.
      build_args = []
      args = options.fetch('args', {})

      # Pull out `BuildRequires:` packages and add them to a `packages`
      # build argument for the container if they exist.
      if options.fetch('buildrequires', false)
        spec_file = options.fetch(
          'spec_file', "SPECS/#{name.gsub('rpmbuild-', '')}.spec"
        )
        build_packages = build_requirements(spec_file)
        if build_packages
          build_args << '--build-arg'
          build_args << "packages=#{build_packages.join(' ')}"
        end
      end

      args.each do |arg, value|
        build_args << '--build-arg'
        build_args << "#{arg}=#{value}"
      end

      # Add any tags to the build arguments.
      image_name = "#{$project}_#{name}"

      options.fetch('tags', ['latest']).each do |tag|
        build_args << '--tag'
        build_args << "#{image_name}:#{tag}"
      end

      # Setting provisioner parameters.
      d.build_args = build_args

      # Set up basic container settings.
      d.dockerfile = options.fetch('dockerfile', "docker/Dockerfile.#{name}")
      d.remains_running = options.fetch('remains_running', false)
    end
  end
end


# Configure a container to be run from another image to execute `rpmbuild`.
def rpmbuild(config, name, options)
  autostart = options.fetch('autostart', false)
  config.vm.define name, autostart: autostart do |container|
    shared_folders(container, name, options, rpmbuild: true)

    image_name = "#{$project}_#{options['image']}"

    container.vm.provider :docker do |d|
      d.image = image_name

      # Add `--rm` to the creation args so we don't need to keep the container
      # (its image is ran just to compile the RPM).
      d.create_args = options.fetch(
        'create_args', ['--rm']
      )
      d.remains_running = options.fetch(
        'remains_running', true
      )

      # Start constructing the `rpmbuild` command.
      rpmbuild_cmd = ['rpmbuild']

      # Pass in the RPM version/release information via CLI define statements.
      if options.key?('release')
        version = options['version']
        release = options['release']
      else
        version, release = options['version'].split('-')
      end
      defines = options.fetch('defines', {})
      defines.update(
        {
          'rpmbuild_version' => version,
          'rpmbuild_release' => release,
        }
      )
      defines.each do |macro, expr|
        rpmbuild_cmd << '--define'
        rpmbuild_cmd << "#{macro} #{expr}"
      end

      # Pass through any variables we want to undefine; by default,
      # we allow `rpmbuild` to retrieve the source.
      options.fetch('undefines', ['_disable_source_fetch']).each do |macro|
        rpmbuild_cmd << '--undefine'
        rpmbuild_cmd << macro
      end

      # Set any with/without options.
      options.fetch('with', []).each do |with_option|
        rpmbuild_cmd << '--with'
        rpmbuild_cmd << with_option
      end

      options.fetch('without', []).each do |without_option|
        rpmbuild_cmd << '--without'
        rpmbuild_cmd << without_option
      end

      # Default to using `rpmbuild -bb`.
      rpmbuild_cmd << options.fetch('build_type', '-bb')
      if options.fetch('nocheck', false)
        rpmbuild_cmd << '--nocheck'
      end
      rpmbuild_cmd << options.fetch('spec_file', "SPECS/#{name}.spec")

      d.cmd = rpmbuild_cmd
    end
  end
end

## Vagrant configuration

Vagrant.configure(2) do |config|
  $images['base'].each do |name, options|
    build_container(config, name, options)
  end

  collect_rpms(
    ['rpmbuild-generic']
  ).each do |name, options|
    rpmbuild(config, name, options)
  end
end
