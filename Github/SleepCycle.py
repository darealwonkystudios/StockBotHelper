import oci
import base64
import tempfile

# -------------------------------
# Authenticate using Instance Principals
# -------------------------------
print("Authenticating using Instance Principals...")
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

# -------------------------------
# Vault secret access (optional)
# -------------------------------
# Replace this with your secret OCID if you need to fetch a key
secret_id = "ocid1.vaultsecret.oc1.ca-toronto-1.amaaaaaavcvqqaqaoolhuxzifpokmj2brdsxtbbx2cnzmelrwjwd3dwpfxka"
print("temp1")
try:
    secrets_client = oci.secrets.SecretsClient(config={}, signer=signer)
    get_secret_response = secrets_client.get_secret_bundle(secret_id)
    secret_content = get_secret_response.data.secret_bundle_content.content
    private_key_pem = base64.b64decode(secret_content).decode("utf-8")

    # Write key to a temporary file (if you need a key file)
    with tempfile.NamedTemporaryFile(delete=False) as key_file:
        key_file.write(private_key_pem.encode("utf-8"))
        key_file_path = key_file.name

    print("Private key loaded from Vault and written to temp file:", key_file_path)

except oci.exceptions.ServiceError as e:
    print("Could not fetch secret from Vault:", e)
    key_file_path = None

print("tem2")

# -------------------------------
# Create Compute Client
# -------------------------------
compute_client = oci.core.ComputeClient(config={}, signer=signer)

# -------------------------------
# Start or Stop an instance
# -------------------------------
# Replace with your VM OCID
instance_ocid = "ocid1.instance.oc1.ca-toronto-1.an2g6ljrvcvqqaqc5gt4j5u7lrtjgx5u66qskxuopbdidghgz6zm2v7ctn3a"

# Example: start the instance
compute_client.instance_action(instance_ocid, "START")
print(f"Instance {instance_ocid} started.")

# Example: stop the instance
# compute_client.instance_action(instance_ocid, "STOP")
# print(f"Instance {instance_ocid} stopped.")