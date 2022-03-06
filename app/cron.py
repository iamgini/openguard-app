from .import models
import json
from datetime import datetime
import ansible_runner
from .serializers import ManagedNodesSerializer

def my_cron_job():
    # your functionality goes here
    ## get first tow
    #all_incidents = models.Incidents.objects.all().order_by('incident_time').first()

    ## get n rows
    all_incidents = models.Incidents.objects.all().filter(incident_status='PENDING').order_by('incident_time')[0:3]
    #all_incidents = models.Incidents.objects.all()
    #print(all_incidents)
    dateTimeObj = datetime.now()
    timestampStr = str(dateTimeObj.strftime("%Y-%b-%d-%H:%M:%S"))
    for incident in all_incidents.iterator():
        #print(incident.incident_rule)

        this_hostname=incident.incident_hostname
        rule_detected=incident.incident_rule

        managed_node = models.ManagedNodes.objects.all().filter(instance_name=this_hostname).order_by('instance_name').first()
        print(managed_node)
        node_connection_name = getattr(managed_node,'instance_credential')
        node_connection_method = getattr(managed_node,'instance_name_connection')
        
        try:
            rule_list = models.Rules.objects.all().filter(rule_name =   rule_detected).order_by('rule_name').first()
            rule_fix_playbook = getattr(rule_list,'rule_fix_playbook')
            #print(rule_fix_playbook)

            ## Call Ansible Runner
            run_ansible(this_hostname, node_connection_method, 'test.yml')

        #managenodes_serializer = ManagedNodesSerializer(data=managed_node)
        #if managenodes_serializer.is_valid():
        #    print(managenodes_serializer.data)
        #for node in managed_node.iterator():
        #    print(managed_node.instance_name)
            new_log = open( 'application_logs/logs', "a")
            new_log.write('\n' + timestampStr + ": " + str(incident.    incident_hostname) + "/" + incident.incident_rule + "/" + str   (incident.incident_time))
            #new_log.write('\n'  + json.dumps( incident.    #incident_time_reported ))
            new_log.close()
        except:
            print("No rules found")
## Ansible runner 
def run_ansible(node_names, ansible_host_name, playbook_file):

    ## varialble
    inventory_file = 'ansible_data/inventory/this_inventory'
    ## create inventory
    #hosts = {
    #    'hosts': {
    #        'Ubuntu-20-CP': {
    #            'ansible_host': '192.168.56.35',
    #            'ansible_user': 'devops',
    #            'ansible_password': 'devops'
    #        }
    #    },
    #}
    #print(hosts)
    
    ## create file manually due to persmission issue
    this_inventory = node_names + " ansible_host=" + ansible_host_name + " ansible_user=devops ansible_password=devops "
    print(this_inventory)
    new_inventory = open(inventory_file, "w")
    new_inventory.write(this_inventory)
    new_inventory.close()

    ## fetch and assign extra variables
    extravars = {
        'NODES': node_names
    }

    ## build kwargs for passing to runner
    kwargs = {
        'playbook': playbook_file,
        #'inventory': {'all': hosts},
        #'inventory': inventory_file,
        #'envvars': envvars,
        'extravars': extravars,
        'private_data_dir': 'ansible_data'
    }

    #ansiblerunner = ansible_runner.run(private_data_dir='ansible_data', 
    #                       playbook='test.yml')

    ## run ansible_runner with **kwargs
    ansiblerunner = ansible_runner.run(**kwargs)

    print("{}: {}".format(ansiblerunner.status, ansiblerunner.rc))
    # successful: 0
    for each_host_event in ansiblerunner.events:
        print(each_host_event['event'])
    print("Final status:")
    print(ansiblerunner.stats)

#run_ansible('localhost', 'test.yml')