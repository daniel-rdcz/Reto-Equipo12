using System.Collections;
using UnityEngine;

public class Semaforo : MonoBehaviour
{
    public GameObject luz;

    public Transform posVerde;
    public Transform posAmarilla;
    public Transform posRoja;

    public float direction;

    private bool verde;
    private bool amarilloDesdeVerde;
    private bool amarilloDesdeRoja;
    private bool roja;

    private void Start()
    {
        verde = true;

        // Agrega la rotación en el eje Y según el valor de 'direction'
        
    }

    void Update()
    {
        transform.rotation = Quaternion.Euler(-90f, direction, 0f);
        if(verde)
        {
            luz.transform.position = posVerde.position;
            luz.GetComponent<Light>().color = new Color32(61, 161, 27, 255);
            StartCoroutine(luzVerde());
            amarilloDesdeRoja = false;
        }

        if(amarilloDesdeVerde)
        {
            luz.transform.position = posAmarilla.position;
            luz.GetComponent<Light>().color = Color.yellow;
            StartCoroutine(luzAmarillaV());
            verde = false;
        }

        if(amarilloDesdeRoja)
        {
            luz.transform.position = posAmarilla.position;
            luz.GetComponent<Light>().color = Color.yellow;
            StartCoroutine(luzAmarillaR());
            roja = false;
        }

        if(roja)
        {
            luz.transform.position = posRoja.position;
            luz.GetComponent<Light>().color = Color.red;
            StartCoroutine(luzRoja());
            amarilloDesdeVerde = false;
        }
    }

    IEnumerator luzVerde()
    {
        yield return new WaitForSeconds(10);
        amarilloDesdeVerde = true;
    }

    IEnumerator luzAmarillaV()
    {
        yield return new WaitForSeconds(3);
        roja = true;
    }

    IEnumerator luzAmarillaR()
    {
        yield return new WaitForSeconds(3);
        verde = true;
    }

    IEnumerator luzRoja()
    {
        yield return new WaitForSeconds(10);
        amarilloDesdeRoja = true;
    }
}
