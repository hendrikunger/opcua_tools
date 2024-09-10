#%%
import asyncua

print(asyncua.__version__)
# %%
import asyncio

from asyncua import Client

url = "opc.tcp://172.16.100.6:8021"
namespace = "urn:WIN-IBKT0GFPRI7:XdcOpcua"
transcation_types = ["SER", "BOX", "DAT", "PAC", "HMIAddKomp", "HMIData", "TRA", "USR", "OEE"]


async def main():

    print(f"Connecting to {url} ...")
    client = Client(url=url)
    client.set_user("VDC01")
    client.set_password("Vdc01C123")
    client.session_timeout = 100000
    await client.connect()
    nsidx = await client.get_namespace_index(namespace)
    print(f"Namespace Index for '{namespace}': {nsidx}")
    mesroot = client.get_node("ns=2;s=C1")
    print(f"MES Root Adress: {mesroot}")
    print("")
    machines = await mesroot.get_children()
    for machine in machines:
        machine_name = (await machine.read_display_name()).Text
        print(machine_name)
        transactions = await machine.get_children()
        for transaction in transactions:
            transaction_name = (await transaction.read_display_name()).Text
            print(f"   {transaction_name}")
            if transaction_name in transcation_types:
                trans_data = await transaction.get_children()
                for node_data in trans_data:
                    node_data_name = (await node_data.read_display_name()).Text
                    node_data_value = await node_data.read_value()
                    print(f"      {node_data_name}")
                    if type(node_data_value) == list:
                        for element in node_data_value:
                            print(f"         {element}")
                    else:
                        print(f"         {node_data_value}")


    await client.disconnect()



await main()



# %%
