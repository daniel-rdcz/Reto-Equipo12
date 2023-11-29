using System.Collections;
using UnityEngine;

public class Semaforo : MonoBehaviour
{
    public GameObject luz;

    public Transform posVerde;
    public Transform posRoja;

    public float direction;

    public bool color;

    void Update()
    {
        // No se necesita la lógica de cambio de color aquí
        // Solo actualizamos el color cuando cambiamos la variable 'verde'
        transform.rotation = Quaternion.Euler(-90f, direction, 0f);
        if (color)
        {
            luz.transform.position = posVerde.position;
            luz.GetComponent<Light>().color = new Color32(61, 161, 27, 255);
        }
        else
        {
            luz.transform.position = posRoja.position;
            luz.GetComponent<Light>().color = Color.red;
        }
    }

}
