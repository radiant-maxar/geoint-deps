# Bootstrap Enterprise Linux Repository

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
   cp -pv RPMS/{noarch,x86_64}/*.rpm el9/stable
   ./scripts/repo-update.sh el9/stable
   ./scripts/repo-sign.sh el9/stable
   ```

   Exit the container and upload:

   ```
   aws s3 sync el9/stable/ s3://geoint-deps/el9/stable/ --delete --profile gaasdg
   ```

1. Create the intermediate stage of RPMs necessary:

    ```
    make libosmium postgis rack
    ```

    Sign the new RPMs, and update the repository:

    ```
    rpm --addsign RPMS/noarch/libosmium-devel-*.rpm RPMS/noarch/rubygem-rack-*.rpm RPMS/x86_64/postgis-*.rpm
    cp -pv RPMS/noarch/libosmium-devel-*.rpm RPMS/noarch/rubygem-rack-*.rpm RPMS/x86_64/postgis-*.rpm el9/stable
    ./scripts/repo-update.sh el9/stable
    ./scripts/repo-sign.sh el9/stable
    ```

    Sync back up again:

    ```
    aws s3 sync el9/stable/ s3://geoint-deps/el9/stable/ --delete --profile gaasdg
    ```

1. Finally, create `mapnik`:

    ```
    make mapnik
    ```

    Sign the `mapnik` RPMs, and update the `el9/stable` repository with them:

    ```
    rpm --addsign RPMS/x86_64/mapnik-*.rpm
    cp -pv RPMS/x86_64/mapnik-*.rpm el9/stable
    ./scripts/repo-update.sh el9/stable
    ./scripts/repo-sign.sh el9/stable
    ```

    Sync back up again:

    ```
    aws s3 sync el9/stable/ s3://geoint-deps/el9/stable/ --delete --profile gaasdg
    ```

1.  Now the repository is bootstrapped, all other RPMs may be created:

    ```
    make all-rpms
    ```
