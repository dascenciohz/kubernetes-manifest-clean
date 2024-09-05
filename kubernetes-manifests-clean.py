#!/usr/bin/env python3

import sys
import yaml
import os

filtered_resources = []

FIELDS_TO_RM = {
    "metadata": {
        "annotations": {
            "kubectl.kubernetes.io/last-applied-configuration": " ",
            "autoscaling.alpha.kubernetes.io/conditions": " ",
            "control-plane.alpha.kubernetes.io/leader": " "
        },
        "generation": " ",
        "creationTimestamp": " ",
        "resourceVersion": " ",
        "selfLink": " ",
        "uid": " ",
        "managedFields": " "
    },
    "spec": {
        "clusterIP": " ",
        "clusterIPs": " ",
        "finalizers": " "
    },
    "status": " "
}

def remove_fields(rm, d):
    for k in rm.keys():
        if k in d.keys():
            if isinstance(rm[k], dict):
                remove_fields(rm[k], d=d[k])
            else:
                del d[k]
    return d

def write_manifest_clear(path, namespace, filename, data):
    manifest_path = os.path.join(path, namespace)
    if not os.path.exists(manifest_path):
        os.makedirs(manifest_path)
        print(f"Directorio '{manifest_path}' creado.")
    else:
        print(f"Directorio '{manifest_path}' ya existe.")
    ruta_archivo = os.path.join(manifest_path, filename)
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(data)
    print(f"Manifiesto YAML '{ruta_archivo}' creado y guardado.")

def manifests_clear(path, new_path):
    try:
        elements = os.listdir(path)
        directories = [element for element in elements if os.path.isdir(os.path.join(path, element))]
        for directory in directories:
            try:
                manifest_path = f"{path}/{directory}"
                directory_elements = os.listdir(manifest_path)
                manifests = [manifest_element for manifest_element in directory_elements if os.path.isfile(os.path.join(manifest_path, manifest_element))]
                for manifest in manifests:
                    with open(f"{manifest_path}/{manifest}", "r") as file_yaml:
                        manifest_yaml = yaml.safe_load(file_yaml)
                    if "items" in manifest_yaml:
                        for resource in manifest_yaml["items"]:
                            filtered_resources.append(remove_fields(FIELDS_TO_RM, resource))
                        manifest_yaml["items"] = filtered_resources
                    else:
                        manifest_yaml = remove_fields(FIELDS_TO_RM, manifest_yaml)
                    manifest_name = f"{manifest_yaml["kind"]}-{manifest_yaml["metadata"]["name"]}.yaml"
                    manifest_data = yaml.dump(manifest_yaml, default_flow_style=False)
                    write_manifest_clear(new_path, directory, manifest_name, manifest_data)
            except PermissionError:
                print(f"(2) No tienes permiso para acceder a la ruta {f"{path}/{directory}"}.")
    except FileNotFoundError:
        print(f"(1) La ruta {path} no existe.")
    except PermissionError:
        print(f"(1) No tienes permiso para acceder a la ruta {path}.")

if __name__ == "__main__":
    if not sys.stdin.isatty():
        resources = yaml.full_load(sys.stdin)
    else:
        try:
            input_dirname = sys.argv[1]
            input_new_dirname = sys.argv[2]
        except IndexError:
            message = '\n[!] Se requieren 2 argumentos para su ejecución: \n\tArg1: Nombre del directorio con todos los YAML a limpiar.\n\tArg2: Nombre del nuevo directorio donde serán escritos los YAML limpios.'
            raise IndexError(message)
        else:
            manifests_clear(input_dirname, input_new_dirname)
