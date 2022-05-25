# Bootstrap new Enterprise Linux Version

1. Create basic geospatial dependencies and libraries:

   ```
   make gdal iniparser libpqxx protozero
   ```

1. Create and upload repository by starting `rpmbuild-generic` container:

   ```
   mkdir -p el9/stable
   docker run \
   -v $HOME/.gnupg-geoint:/rpmbuild/.gnupg:rw \
   -v $(pwd)/RPMS:/rpmbuild/RPMS:rw \
   -v $(pwd)/el9:/rpmbuild/el9:rw \
   -v $(pwd)/scripts:/rpmbuild/scripts:ro \
   -it --rm deps-stable-el9_rpmbuild-generic
   ```

   Then signing RPMs:

   ```
   rpm --addsign RPMS/{noarch,x86_64}/*.rpm
   ./scripts/repo-update.sh el9/stable
   ```

   Exit the container and upload:

   ```
   aws s3 sync el9/stable/ s3://geoint-deps/el9/stable/ --profile gaasdg
   ```

1. Create `libosmium` and `postgis`:

  ```
  make libosmium postgis
  ```

  Sign the `libosmium-devel` and `postgis` RPMs, and update the `el9/stable` repository with them.
