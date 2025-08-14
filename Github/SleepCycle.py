import oci
import base64
import tempfile
import datetime as dt
import time

def toggle_big_state(IsStart):

    print("Authenticating using Instance Principals...")
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

    # Access api key to shut off instance from vault 
    # Replace this with your secret OCID if you need to fetch a key
    
    secret_id = "ocid1.vaultsecret.oc1.ca-toronto-1.amaaaaaavcvqqaqaoolhuxzifpokmj2brdsxtbbx2cnzmelrwjwd3dwpfxka"
    
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

    compute_client = oci.core.ComputeClient(config={}, signer=signer)

    instance_ocid = "ocid1.instance.oc1.ca-toronto-1.an2g6ljrvcvqqaqc5gt4j5u7lrtjgx5u66qskxuopbdidghgz6zm2v7ctn3a"


    if IsStart:
        compute_client.instance_action(instance_ocid, "START")
    else:
        compute_client.instance_action(instance_ocid, "SOFTSTOP")
    print(f"Instance {instance_ocid} started.")


while False:     
    now = dt.datetime.now()
    target = now.replace(hour=8, minute=0, second=0, microsecond=0)

    # If it's already past 8 AM today, target should be tomorrow at 8 AM
    if now >= target:
        target += dt.timedelta(days=1)

    seconds_to_sleep = (target - now).total_seconds()

    time.sleep(seconds_to_sleep) # sleep until 8 AM

    print("Turning instance on...")
    toggle_big_state(True)
    
    now = dt.datetime.now()
    target = now.replace(hour=16, minute=0, second=0, microsecond=0)

    seconds_to_sleep = (target - now).total_seconds()

    time.sleep(seconds_to_sleep + 600) # sleep until 4 PM + 10 minutes as a buffer

    print("Turning instance off...")
    toggle_big_state(False)

print ("Script ended")

toggle_big_state(True)

