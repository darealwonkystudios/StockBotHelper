import oci
import tempfile
import base64
# Use instance principals to avoid storing creds locally
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

# Create Vault client
secrets_client = oci.secrets.SecretsClient(config={}, signer=signer)

# OCID of the secret from Vault Console
secret_id = "ocid1.vaultsecret.oc1.ca-toronto-1.amaaaaaavcvqqaqaoolhuxzifpokmj2brdsxtbbx2cnzmelrwjwd3dwpfxka"

# Get the secret bundle
get_secret_response = secrets_client.get_secret_bundle(secret_id)

# Extract the key content
secret_content = get_secret_response.data.secret_bundle_content.content
private_key_pem = base64.b64decode(secret_content).decode("utf-8")

print("Private key loaded from Vault:")
print(private_key_pem)


# Write key to a temp file in memory-safe way
with tempfile.NamedTemporaryFile(delete=False) as key_file:
    key_file.write(private_key_pem.encode("utf-8"))
    key_file_path = key_file.name

config = {
    "user": "ocid1.user.oc1..aaaaaaaaubzm3qcl2j54amchy2v4hrzaohzxhpvcfmj6ptqtc6c2tzqbzelq",
    "fingerprint": "19:26:57:30:94:27:83:81:01:2e:77:f1:83:5a:25:d3",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaanpptjh3zuc6p6xfby3t5hn667oernezt5xadozkwys4nes5yu4iaregion=ca-toronto-1",
    "region": "ca-toronto-1",
    "key_file": key_file_path
}

compute_client = oci.core.ComputeClient(config)
compute_client.instance_action("<BIG_VM_OCID>", "START")
print("Big VM stopped")