touch /dev/shm/geoint-passphrase.txt
chmod 0600 /dev/shm/geoint-passphrase.txt
dd if=/dev/urandom of=/dev/stdout bs=128 count=1 | base64 -w 0 > /dev/shm/geoint-passphrase.txt

time ./rpm_gpg_keygen.py \
  --key-dest $HOME/.gnupg-geoint \
  --key-email foundationgeoint-packaging@maxar.com \
  --key-name "FoundationGEOINT Packaging" \
  --passphrase-file /dev/shm/geoint-passphrase.txt

gpg --homedir $HOME/.gnupg-geoint --export --armor > $HOME/geoint.gpg
tar -C $HOME -cJvf gnupg-geoint.tar.xz geoint.gpg .gnupg-geoint

docker run \
 -v ${HOME}/.gnupg-geoint:/rpmbuild/.gnupg:rw \
 -v /dev/shm/geoint-passphrase-2.txt:/dev/shm/geoint-passphrase.txt:ro \
 -v $(pwd)/scripts:/rpmbuild/scripts:ro \
 -v $(pwd)/RPMS:/rpmbuild/RPMS:rw \
 -v $(pwd)/el7:/rpmbuild/el7:rw \
 -it --rm deps-stable_rpmbuild-generic

%_gpg_digest_algo sha512
%_gpg_name FoundationGEOINT Packaging
%_gpg_password_file /dev/shm/geoint-passphrase.txt
%_gpg_path /rpmbuild/.gnupg
%__gpg_sign_cmd %{__gpg} \
  gpg --batch --no-verbose --no-armor --pinentry-mode loopback --passphrase-file %{_gpg_password_file} \
  %{?_gpg_digest_algo:--digest-algo %{_gpg_digest_algo}} \
  --no-secmem-warning \
  -u "%{_gpg_name}" -sbo %{__signature_filename} %{__plaintext_filename}
