from synapseclient.exceptions import *

## Synapse user IDs of the challenge admins who will be notified by email
## about errors in the scoring script
ADMIN_USER_IDS = ['3324230']

def validate_submission(syn, evaluation, submission, public=False, admin=None):
    """
    Find the right validation function and validate the submission.

    :returns: (True, message) if validated, (False, message) if
              validation fails or throws exception
    """
    print 'in validate_submission: public='+str(public)+", admin="+str(admin)
    try:
        if public:
            ent = syn.getPermissions(submission['entityId'])
            assert "READ" in ent and "DOWNLOAD" in ent, "Please share your private directory (%s) with the `Public` with `Can Download` permissions." % submission['entityId']
        if admin is not None:
            ent = syn.getPermissions(submission['entityId'], admin)
            assert "READ" in ent and "DOWNLOAD" in ent, "Please share your private directory (%s) with the Synapse user `%s` with `Can Download` permissions." % (submission['entityId'], admin)           
    except SynapseHTTPError as e:
        if e.response.status_code == 403:
            raise AssertionError("Please share your private directory (%s) with the Synapse user `%s` with `Can Download` permissions." % (submission['entityId'], admin))
        else:
            raise(e)
    return True, "Validated!"

