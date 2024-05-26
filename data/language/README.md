# 🖋 Translating Imaginary
- Translating Imaginary has some process to do (sorry)

## Translate List
| JSON Name              	| Default Text                            	| Location                     	| Widget                  	| Usage                                          	|
|------------------------	|-----------------------------------------	|------------------------------	|-------------------------	|------------------------------------------------	|
| langName               	| en_US                                   	| None                         	| None                    	| Language Name Information                      	|
| NO_ARGUMENTS_FOUND     	| No Startup Option is provided           	| main.py                      	| label_VMInfo            	| Startup Arguments Not found                    	|
| NO_DESCRTIPION_FOUND   	| No Description is provided              	| main.py                      	| label_Vm_Desc           	| VM Description Text Not found                  	|
| NO_METADATA_FOUND      	| Cannot found Guest Metadata information 	| main.py                      	| label_VMInfo            	| Metadata Information Invaild                   	|
| NO_VM_AVALIABLE        	| No VM has been found                    	| main.py                      	| label_Vm_Title          	| No Vm found (skip driver folder)               	|
| NO_VM_AVALIABLE_DESC   	| How about making new one?               	| main.py                      	| label_Vm_Desc           	| No Vm found (skip driver folder)               	|
| DUMMY                  	| Dummy                                 	| None                         	| None                    	| Dummy Dev Text                                 	|
| SELECT_VM              	| Select Vm to Start!                     	| main.py                      	| label_Vm_Title          	| VM Found but not selected                      	|
| CREATE_VM              	| Create VM                               	| main.py                      	| createVM                	| VM Creation Button                             	|
| IMAGINARY_INFO         	| Info                                    	| main.py                      	| setting                 	| Imaginary Information (Lang Setting page)      	|
| DISK_TOOL              	| Disk Tool                               	| main.py                      	| diskTool                	| Disk Tool Button                               	|
| FORCE_RELOAD_LIST      	| Force Reload VM List                    	| main.py                      	| imaginarySetting        	| Reload VM Guest List View                      	|
| UNKNOWN_DISK           	| Unknown Disk                            	| main.py                      	| None (VM Metadata JSON) 	| Unknown Disk Loaded                            	|
| MAIN_STATUS_NULL       	| Status: No VM Status has been found     	| main.py                      	| label_Vm_Status         	| VM Status Invaild (Invaild Process, Exception) 	|
| MAIN_STATUS_RUNNING    	| Status: Running through resistance..    	| main.py                      	| label_Vm_Status         	| VM Process found, Running                      	|
| MAIN_VMSTART           	| Start VM                                	| main.py                      	| runVM                   	| VM Run Button                                  	|
| MAIN_VMEDIT            	| Edit VM                                 	| main.py                      	| editVM                  	| VM Edit Button                                 	|
| CREATEVM_1_TITLE       	| VM Setup                                	| src/gui/createvm/createvm.py 	| label_Title             	| VM Setup Title Frame 1                         	|
| CREATEVM_2_TITLE       	| Disk Setup                              	| src/gui/createvm/createvm.py 	| label_Title             	| VM Setup Title Frame 2                         	|
| CREATEVM_3_TITLE       	| Etc                                     	| src/gui/createvm/createvm.py 	| label_Title             	| VM Setup Title Frame 3                         	|
| CREATEVM_LABEL_VMNAME  	| VM Name                                 	| src/gui/createvm/createvm.py 	| label_InputLabel     	    | VM Setup Guest Name Label                      	|
| CREATEVM_LABEL_VMDESC  	| VM Description                          	| src/gui/createvm/createvm.py 	| label_loadISO           	| VM Setup Guest VM Description Label               |
| CREATEVM_TITLE_LOADISO 	| ISO Location                            	| src/gui/createvm/createvm.py 	| label_loadISO_title     	| VM Setup ISO Load Title                           |
| CREATEVM_DISKTYPE_RAW 	| RAW : Biggest but, fastest Disk type.     | src/gui/createvm/createvm.py 	| diskType_RAW           	| Virtual Disk Type RAW                             |

- others will be added soon(tm)