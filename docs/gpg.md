# GPG Tools

## RPM GPG Key Generation

The [`rpm_gpg_keygen.py`](../scripts/rpm_gpg_keygen.py) script generates GnuPG
keys with sane defaults compatible for use with signing RPMs.

### Requirements

In general, you'll need the [`python-gnupg`](https://pypi.org/project/python-gnupg/)
package.  If you're in a container or virtual machine, your entropy sources may be limited;
in that case the [`rng-tools`](https://github.com/nhorman/rng-tools) should be installed
as well.  Fortunately, these are both available as system packages on CentOS
and Ubuntu.

CentOS:
* `epel-release`
* `python2-gnupg`
* `rng-tools` (start service with `sudo systemctl start rngd`)

Ubuntu:
* `python3-gnupg`
* `rng-tools` (start service with `sudo systemctl start rng-tools`)

### Usage

Choose or generate a passphrase, ensure it's in a location you won't forget:

```
touch /dev/shm/rpmbuild-passphrase.txt
chmod 0600 /dev/shm/rpmbuild-passphrase.txt
dd if=/dev/urandom of=/dev/stdout bs=128 count=1 | base64 -w 0 > /dev/shm/rpmbuild-passphrase.txt
```

The example below creates a GnuPG keyring in `$HOME/.gnupg-geoint` with the identity
`FoundationGEOINT Packaging <foundationgeoint-packaging@maxar.com>`:

```
time ./scripts/rpm_gpg_keygen.py \
  --key-dest $HOME/.gnupg-geoint \
  --key-name "FoundationGEOINT Packaging" \
  --key-email foundationgeoint-packaging@maxar.com \
  --passphrase-file /dev/shm/rpmbuild-passphrase.txt
```

Key details can be verified with the following:
```
gpg --homedir $HOME/.gnupg-geoint --list-keys --with-colons
```

Export an ASCII "armored" version of the key, this is how Yum/RPM consumes public keys:
```
gpg --homedir $HOME/.gnupg-geoint --export --armor > $HOME/geoint.gpg
```

Create a tarball for distribution, keep passphrase out of it:
```
tar -C $HOME -cJvf SOURCES/gnupg-geoint.tar.xz geoint.gpg .gnupg-geoint
```

### Additional Information

RPM signing is finicky -- subkeys can't be used, v4 signatures aren't accepted
on legacy platforms, and GnuPG is user-hostile.  This script aims to have some
sane defaults:

* 4096-bit RSA keys are the default.
* High-quality algorithm order embedded in GnuPG key preferences (e.g., only use SHA-2 digest algorithms).
* Key usage limited to signing only.


### References

* [Applied Crypto Hardening's example GnuPG configuration](https://github.com/BetterCrypto/Applied-Crypto-Hardening/tree/master/src/configuration/GPG/GnuPG).

* [Riseup's OpenPGP Best Practices](https://riseup.net/en/security/message-security/openpgp/gpg-best-practices); even though the guide is deprecated it still applies because CentOS 7 use GnuPG 2.0 (2.1 is more sane).
* [Jacob Applebaum's "duraconf" gpg.conf](https://github.com/ioerror/duraconf/blob/master/configs/gnupg/gpg.conf).
* [Sigul](https://pagure.io/sigul), Fedora's RPM signing system.
