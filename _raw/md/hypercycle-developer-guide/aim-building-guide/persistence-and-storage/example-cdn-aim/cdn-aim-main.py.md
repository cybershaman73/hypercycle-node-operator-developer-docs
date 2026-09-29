> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-developer-guide/aim-building-guide/persistence-and-storage/example-cdn-aim/cdn-aim-main.py.md).

# CDN AIM main.py

Content Delivery Network (CDN) AIM main.py example used to demonstrate SubscriptionManager, DiskSpaceManager and StorageManager services within the Node Manager.

```python
import os
import hashlib
import asyncio
from pyhypercycle_aim import JSONResponseCORS, HTMLResponseCORS, SimpleServer, aim_uri, SubscriptionManager

PORT = int(os.environ.get('PORT', 4000))

## Helper function
def remove_empty_dirs(path, keep_path=None):
    path = os.path.abspath(path)
    keep_path = os.path.abspath(keep_path) if keep_path else None

    while True:
        if keep_path and os.path.samefile(path, keep_path):
            break
        try:
            os.rmdir(path)  # Remove if empty
            print(f"Removed: {path}")
            path = os.path.dirname(path)
        except OSError:
            break  # Not empty or doesn't exist

class DiskSubscription(SubscriptionManager):
    @classmethod
    def remove_callback(cls, key):
        subscription = cls.get_subscription(key)
        DiskSpaceManager.remove_disk("1K", size//1024, disk_id)

class CDNExample(SimpleServer):
    manifest = {
        "name": "CDN Example Aim",
        "short_name": "cdn-example",
        "version": "0.1",
        "documentation_url": "...",
        "license": "Open",
        "terms_of_service": "",
        "author": "Barry Rowe",
        "suggested_costs": {
            "StorageUnits": {"currency": "USDC", "amount": 1000000,
                          "description": "Amount to charge per month per GB. Suggested $1.00 USD."},
            "BandwidthUnits": {"currency": "USDC", "amount": 30000,
                           "description": "Amount to charge per GB of bandwidth. Suggested $0.03 USD/GB."},

    }
    disk_to_user_address = {}

    @aim_uri(uri="/allocate", methods=["POST"],
             endpoint_manifest = {
                 "input_query": "",
                 "input_headers": {},
                 "input_body": {"disk": {"space": "<Int>", "name": "<String>", "months": "<Int>"},
                                "bandwidth": "<Int|null>"},
                 "output": {"status": "<String>"},
                 "documentation": "Allocates disk space and bandwidth for a user account to for serving CDN requests.",
                 "example_calls": [{
                     "body": {"disk": {"space": 1000000000, "name": "my-site", "months": 1}},
                     "method": "POST",
                     "query": "",
                     "headers": "",
                     "output": {"status": "ok"}
                 }, {
                     "body": {"bandwidth": 2000000000},
                     "method": "POST",
                     "query": "",
                     "headers": "",
                     "output": {"status": "ok"}
                 }]
    })
    async def allocate(self, request):
        body = await request.json()
        costs = []
        costs_only = []
        bandwidth = body.get("bandwidth",0)
        disk = body.get("disk",{})
        if bandwidth:
            costs.append({"currency": "BandwidthUnits", "used": bandwidth})
            costs_only.append({"currency": "BandwidthUnits", "min": bandwidth,
                               "max": bandwidth, "estimated": bandwidth})
        if disk:
            disk_space = int(disk.get("space",0))
            months = int(disk.get("months",0))
            if months:
                costs.append({"currency": "StorageUnits", "used": disk_space*months})
                costs_only.append({"currency": "StorageUnits", "min": disk_space*months,
                                   "max": disk_space*months, "estimated": disk_space*months})

        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": costs_only})

        if disk:
            name = disk.get("name","static")
            if not name.isalnum():
                return JSONResponseCORS({"error":"Disk name must be alpha numeric."})

            user_address = self.get_user_address(request)
            key = user_address+"__"+name
            subscription = DiskSubscriptionManager.get_subscription(key)
            if subscription.get("exists") == True and subscription['metadata'].get("space",0) != disk_space:
                return JSONResponseCORS({"error": "Disk already exists. To topup, ensure the 'space' value matches: must be "+str(subscription['metadata'].get("space",0))})
            else:
                disk_id = hashlib(key.encode("utf-8")).hexdigest()
                DiskSubscriptionManager.add_subscription(key,
                        {"address": user_address, "space": space, "name": name, "disk_id": disk_id},
                        delete_on_expire=True, months=months)
                DiskSpaceManager.add_disk("1K", size//1024, disk_id)
        if bandwidth:
            user_address = self.get_user_address(request)
            value = StorageManager.get(user_address, "bandwidth", 0)
            StorageManager.store(user_address, "bandwidth", value+bandwidth)
        return JSONResponseCORS({"status": "ok"}, costs=costs)

    @aim_uri(uri="/get_subscription", methods=["GET"],
             endpoint_manifest = {
                 "input_query": "",
                 "input_headers": {},
                 "input_body": "",
                 "output": {"disks": [{"key": "<UserAddress>__<String>", "metadata": "<Object>",
                                       "deadline": "<Timestamp>", "delete_on_expire": "<Bool>",
                                       "expired": "<Bool>", "exists": "<Bool>"}],
                            "bandwidth": "<Int>"},
                 "documentation": "",
                 "example_calls": [{
                     "input_query": "",
                     "input_headers": {},
                     "input_body": "",
                     "output": {"disks": [{"key": "0x01234...", "metadata": {"address":"0x01234...", "space": 1000000000, "name": "my-disk", "disk_id": "abcd0123..."}, "deadline": 1745372398.0380416,
                        "delete_on_expire": True, "expired": False, "exists": True
                       }], "bandwidth": 1234000000
                     }
                   }
                 ],
    })
    async def get_subscription(self, request):
        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": []})

        user_address = self.get_user_address(request)
        bandwidth_value = StorageManager.get(user_address, "bandwidth", 0)
        disks = []
        for sub in SubscriptionManager.get_all_subscriptions():
           if sub['metadata']["address"] == user_address:
               disks.append(sub)
        data = {"disks": disks, "bandwidth": bandwidth_value}

        return JSONResponseCORS(data, costs=[])

    #/upload_file
    @aim_uri(uri="/upload_file", methods=["POST"],
             endpoint_manifest = {
                 "input_query": "?name=<String>&filename=<String>&path=<String>&delete=<Bool>",
                 "input_headers": {},
                 "input_body": "",
                 "output": {},
                 "documentation": "",
                 "example_calls": [{
                     "input_query": "",
                     "input_headers": {},
                     "input_body": "",
                     "output": {}
                   }
                 ],
    })
    async def update_file(self, request):
        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": []})
        name = request.query_params.get("disk_name","")
        filename = request.query_params.get("filename","").lstrip("/")
        path = request.query_params.get("path","").lstrip("/").rstrip("/")

        delete = bool(request.query_params.get("delete", "false"))

        #validate filename and path
        #...
        user_address = self.get_user_address(request)

        key = user_address+"__"+name
        subscription = DiskSubscriptionManager.get_subscription(key)
        rpath = f"{disk_id}/{path}/{filename}"
        if subscription.get("exists") == True:
            disk_id = subscription['disk_id']
            vpath = f"/container_mount/disk_mounts/{disk_id}/{path}/"
            if delete:
                os.remove(f"{vpath}/{filename}")
                remove_empty_dirs(f"{vpath}", keep_path=f"/container_mount/disk_mounts/{disk_id}")
            else:
                os.makedirs(vpath, exist_ok=True)
                fo = os.write(f"{vpath}/{filename}", "w")
                fo.close()
        else:
            return JSONResponseCORS({"error": f"Disk name for this user does not exist. User: {user_address}, disk: {name}"})
        return JSONResponseCORS({"status": "ok", "path": rpath}, costs=[])

    #/get_file 
    @aim_uri(uri="re:/data/(.*)", methods=["GET"],
             endpoint_manifest = {
                 "input_query": "",
                 "input_headers": {},
                 "input_body": "",
                 "output": {},
                 "documentation": "",
                 "example_calls": [{
                     "input_query": "",
                     "input_headers": {},
                     "input_body": "",
                     "output": {}
                   }
                 ],
                 "is_public": True
    })
    async def data(self, request):
        uri = request.uri.partition("/data/")[2]
        disk, _, path = uri.partition("/")
        if not disk.isalnum():
            return HTMLResponseCORS("Invalid disk", status=404)

        if not disk in cls.disk_to_user_address:
            for sub in DiskSubscriptionManager.get_all_subscriptions():
                if sub('metadata',{}).get("disk_id") == disk:
                    cls.disk_to_user_address[disk] = sub['metadata'].get("address")
        if not disk in cls.disk_to_user_address:
            return HTMLResponse("File not found", status=404)

        #validate path
        #...

        fpath = f"/container_mount/disk_mounts/{disk}/{path}"

        if os.path.exists(fpath):
            user_address = cls.disk_to_user_address[disk]
            data = open(fpath).read()
            bandwdith = len(data)
            filename = fpath.rpartition("/")[2]
            value = StorageManager.get(user_address, "bandwidth", 0)
            if value >= bandwidth:
                StorageManager.store(user_address, "bandwidth", value-bandwidth)
            else:
                return HTMLResponse("Resource bandwidth not allocated.", status=402)
            return FileResponseCORS(data, filename, status=200)
        else:
            return HTMLResponseCORS("File not found.", status=404)

    async def on_startup(self):
        async def loop():
            while True:
                DiskSubscriptionManager.check_all_subscriptions()
                await asyncio.sleep(20)
        asyncio.create_task(loop())


def main():
    app = CDNExample()
    app.run(uvicorn_kwargs={"port": PORT, "host": "0.0.0.0"})

if __name__=='__main__':
    main()
```
