# coding: utf-8
"""*****************************************************************************
* Copyright (C) 2019 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*****************************************************************************"""

############################################################################
#### Cortex-M23-NTZ (No Trust Zone) Architecture specific configuration ####
############################################################################

#CPU Clock Frequency
cpuclk = Database.getSymbolValue("core", "CPU_CLOCK_FREQUENCY")
cpuclk = int(cpuclk)

freeRtosSym_CpuClockHz.setDependencies(freeRtosCpuClockHz, ["core.CPU_CLOCK_FREQUENCY"])
freeRtosSym_CpuClockHz.setDefaultValue(cpuclk)

#Default Heap size
freeRtosSym_TotalHeapSize.setDefaultValue(8192)

# Cortex-M23 does not have a Floating Point Unit (FPU) and therefore configENABLE_FPU must be set to 0
freeRtosSym_EnableFpu.setVisible(False)

#TrustZone configuration
if Variables.get("__TRUSTZONE_ENABLED") != None and Variables.get("__TRUSTZONE_ENABLED") == "true":
    freeRtosSym_EnableTrustZone.setDefaultValue(True)
    freeRtosSym_EnableTrustZone.setVisible(True)
    freeRtosSym_EnableTrustZone.setReadOnly(True)
    freeRtosSym_RunFreeRtosSecure.setVisible(True)
    freeRtosSym_RunFreeRtosSecure.setReadOnly(True)
    freeRtosSym_SecureStackSize.setDefaultValue(1024)
    freeRtosSym_SecureTotalHeapSize.setDefaultValue(1024)

#Enable MPU
freeRtosSym_EnableMpu.setVisible(True)

#Setup Kernel Priority
freeRtosSym_KernelIntrPrio.setDefaultValue(7)
freeRtosSym_KernelIntrPrio.setReadOnly(True)

#Setup Sys Call Priority
freeRtosSym_MaxSysCalIntrPrio.setDefaultValue(1)

#Set SysTick Priority and Lock the Priority
SysTickInterruptIndex        = Interrupt.getInterruptIndex("SysTick")
SysTickInterruptPriority     = "NVIC_"+ str(SysTickInterruptIndex) +"_0_PRIORITY"
SysTickInterruptPriorityLock = "NVIC_" + str(SysTickInterruptIndex) +"_0_PRIORITY_LOCK"

Database.clearSymbolValue("core", SysTickInterruptPriority)
Database.setSymbolValue("core", SysTickInterruptPriority, "3")
Database.clearSymbolValue("core", SysTickInterruptPriorityLock)
Database.setSymbolValue("core", SysTickInterruptPriorityLock, True)

#Set SVCall Priority and Lock the Priority
SVCallInterruptIndex        = Interrupt.getInterruptIndex("SVCall")
SVCallInterruptPriorityLock = "NVIC_" + str(SVCallInterruptIndex) +"_0_PRIORITY_LOCK"

Database.clearSymbolValue("core", SVCallInterruptPriorityLock)
Database.setSymbolValue("core", SVCallInterruptPriorityLock, True)

############################################################################
#### Code Generation ####
############################################################################

configName  = Variables.get("__CONFIGURATION_NAME")

if Variables.get("__TRUSTZONE_ENABLED") != None and Variables.get("__TRUSTZONE_ENABLED") == "true":
    freeRtosDir = "ARM_CM23"
    freeRtosSecureInc = "../../../Secure/firmware/src/third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure;"
else:
    freeRtosDir = "ARM_CM23_NTZ"
    freeRtosSecureInc = ""

freeRtosdefSym = thirdPartyFreeRTOS.createSettingSymbol("FREERTOS_XC32_INCLUDE_DIRS", None)
freeRtosdefSym.setCategory("C32")
freeRtosdefSym.setKey("extra-include-directories")
freeRtosdefSym.setValue("../src/third_party/rtos/FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure;" + freeRtosSecureInc + "../src/third_party/rtos/FreeRTOS/Source/include;")
freeRtosdefSym.setAppend(True, ";")

freeRtosPortSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SAM_PORT_C", None)
freeRtosPortSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/" + freeRtosDir + "/non_secure/port.c")
freeRtosPortSource.setOutputName("port.c")
freeRtosPortSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortSource.setProjectPath("FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortSource.setType("SOURCE")
freeRtosPortSource.setMarkup(False)

freeRtosPortAsmSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SAM_PORTASM_C", None)
freeRtosPortAsmSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/" + freeRtosDir + "/non_secure/portasm.c")
freeRtosPortAsmSource.setOutputName("portasm.c")
freeRtosPortAsmSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortAsmSource.setProjectPath("FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortAsmSource.setType("SOURCE")
freeRtosPortAsmSource.setMarkup(False)

freeRtosPortAsmHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SAM_PORTASM_H", None)
freeRtosPortAsmHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/" + freeRtosDir + "/non_secure/portasm.h")
freeRtosPortAsmHeader.setOutputName("portasm.h")
freeRtosPortAsmHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortAsmHeader.setProjectPath("FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortAsmHeader.setType("HEADER")
freeRtosPortAsmHeader.setMarkup(False)

freeRtosPortHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SAM_PORTMACRO_H", None)
freeRtosPortHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/" + freeRtosDir + "/non_secure/portmacro.h")
freeRtosPortHeader.setOutputName("portmacro.h")
freeRtosPortHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortHeader.setProjectPath("FreeRTOS/Source/portable/GCC/" + freeRtosDir + "/non_secure")
freeRtosPortHeader.setType("HEADER")
freeRtosPortHeader.setMarkup(False)

#If TrustZone Enable
if Variables.get("__TRUSTZONE_ENABLED") != None and Variables.get("__TRUSTZONE_ENABLED") == "true":
    freeRtosSecureIncludeDirSym = thirdPartyFreeRTOS.createSettingSymbol("FREERTOS_XC32_SECURE_INCLUDE_DIRS", None)
    freeRtosSecureIncludeDirSym.setCategory("C32")
    freeRtosSecureIncludeDirSym.setKey("extra-include-directories")
    freeRtosSecureIncludeDirSym.setValue("../src/third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure;../src/third_party/rtos/FreeRTOS/Source/include;../../../NonSecure/firmware/src/config/" + configName + ";")
    freeRtosSecureIncludeDirSym.setAppend(True, ";")
    freeRtosSecureIncludeDirSym.setSecurity("SECURE")

    freeRtosSecureContextSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_CONTEXT_C", None)
    freeRtosSecureContextSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_context.c")
    freeRtosSecureContextSource.setOutputName("secure_context.c")
    freeRtosSecureContextSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextSource.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextSource.setType("SOURCE")
    freeRtosSecureContextSource.setMarkup(False)
    freeRtosSecureContextSource.setSecurity("SECURE")

    freeRtosSecureContextPortSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_CONTEXT_PORT_C", None)
    freeRtosSecureContextPortSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_context_port.c")
    freeRtosSecureContextPortSource.setOutputName("secure_context_port.c")
    freeRtosSecureContextPortSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextPortSource.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextPortSource.setType("SOURCE")
    freeRtosSecureContextPortSource.setMarkup(False)
    freeRtosSecureContextPortSource.setSecurity("SECURE")

    freeRtosSecureHeapSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_HEAP_C", None)
    freeRtosSecureHeapSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_heap.c.ftl")
    freeRtosSecureHeapSource.setOutputName("secure_heap.c")
    freeRtosSecureHeapSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureHeapSource.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureHeapSource.setType("SOURCE")
    freeRtosSecureHeapSource.setMarkup(True)
    freeRtosSecureHeapSource.setSecurity("SECURE")

    freeRtosSecureInitSource = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_INIT_C", None)
    freeRtosSecureInitSource.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_init.c")
    freeRtosSecureInitSource.setOutputName("secure_init.c")
    freeRtosSecureInitSource.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureInitSource.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureInitSource.setType("SOURCE")
    freeRtosSecureInitSource.setMarkup(False)
    freeRtosSecureInitSource.setSecurity("SECURE")

    freeRtosSecureContextHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_CONTEXT_H", None)
    freeRtosSecureContextHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_context.h")
    freeRtosSecureContextHeader.setOutputName("secure_context.h")
    freeRtosSecureContextHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextHeader.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureContextHeader.setType("HEADER")
    freeRtosSecureContextHeader.setMarkup(False)
    freeRtosSecureContextHeader.setSecurity("SECURE")

    freeRtosSecurePortMacrosHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_PORT_MACROS_H", None)
    freeRtosSecurePortMacrosHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_port_macros.h")
    freeRtosSecurePortMacrosHeader.setOutputName("secure_port_macros.h")
    freeRtosSecurePortMacrosHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecurePortMacrosHeader.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecurePortMacrosHeader.setType("HEADER")
    freeRtosSecurePortMacrosHeader.setMarkup(False)
    freeRtosSecurePortMacrosHeader.setSecurity("SECURE")

    freeRtosSecureHeapHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_HEAP_H", None)
    freeRtosSecureHeapHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_heap.h")
    freeRtosSecureHeapHeader.setOutputName("secure_heap.h")
    freeRtosSecureHeapHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureHeapHeader.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureHeapHeader.setType("HEADER")
    freeRtosSecureHeapHeader.setMarkup(False)
    freeRtosSecureHeapHeader.setSecurity("SECURE")

    freeRtosSecureInitHeader = thirdPartyFreeRTOS.createFileSymbol("FREERTOS_SECURE_INIT_H", None)
    freeRtosSecureInitHeader.setSourcePath("config/arch/arm/devices_cortex_m23/src/ARM_CM23/secure/secure_init.h")
    freeRtosSecureInitHeader.setOutputName("secure_init.h")
    freeRtosSecureInitHeader.setDestPath("../../third_party/rtos/FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureInitHeader.setProjectPath("FreeRTOS/Source/portable/GCC/ARM_CM23/secure")
    freeRtosSecureInitHeader.setType("HEADER")
    freeRtosSecureInitHeader.setMarkup(False)
    freeRtosSecureInitHeader.setSecurity("SECURE")
