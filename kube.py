import pykube

# to constroy artifacts in the cluster
def constroy(api,spec):
    if spec["kind"] == 'Deployment':
        pykube.Deployment(api, spec).create()
    if spec["kind"] == 'Service':
        pykube.Service(api, spec).create()
    if spec["kind"] == 'Pod':
        pykube.Pod(api, spec).create()

# to destroy created artifacts
def destroy(api,spec):
    if spec["kind"] == 'Deployment':
        pykube.Deployment(api, spec).delete()
    if spec["kind"] == 'Service':
        pykube.Service(api, spec).delete()
    if spec["kind"] == 'Pod':
        pykube.Pod(api, spec).delete()
        
# scale deployment
def scale_cluster(api,dask_worker_name,n_workers,namespace):
    Deploys = pykube.Deployment.objects(api).filter(namespace=namespace)
    created_workers = list()
    for deploy in Deploys:
        if deploy.name.find(dask_worker_name) != -1:
            deploy.replicas = n_workers
            deploy.update()
            print(deploy.namespace, deploy.name, "replicas", deploy.replicas)
            
def destroy_cluster(api,scheduler_dpl_spec,scheduler_svc_spec,worker_spec):
    destroy(api,scheduler_dpl_spec)
    destroy(api,scheduler_svc_spec)
    destroy(api,worker_spec)