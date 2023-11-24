/*
Use transformation matrices to modify the vertices of a mesh

Gilberto Echeverria
2023-11-02
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    public Vector3 displacement;

    public Vector3 direction;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;
    [SerializeField] GameObject wheelPrefab;
    [SerializeField] int numWheels = 4;

    Mesh mesh;
    Mesh[] meshWheel;
    Vector3[] baseVertices;
    Vector3[] newVertices;
    Vector3[][] baseVerticesWheel;
    Vector3[][] newVerticesWheel;
    Vector3[] wheelCoordinates;



    // Start is called before the first frame update
    void Start()
    {
        // Get the mesh from the child object
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;

        // Create a copy of the original vertices
        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++) {
            newVertices[i] = baseVertices[i];
        }
        baseVerticesWheel = new Vector3[numWheels][];
        newVerticesWheel = new Vector3[numWheels][];
        meshWheel = new Mesh[numWheels];

        for (int x = 0; x < numWheels; x++) {
            GameObject prefabWheel = Instantiate(wheelPrefab, transform.position, Quaternion.identity);
            meshWheel[x] = prefabWheel.GetComponentInChildren<MeshFilter>().mesh;
            baseVerticesWheel[x] = meshWheel[x].vertices;
            newVerticesWheel[x] = new Vector3[baseVerticesWheel[x].Length];
            for (int i = 0; i < baseVerticesWheel.Length; i++) {
                newVerticesWheel[x][i] = baseVerticesWheel[x][i];
            }
        }

        wheelCoordinates = new Vector3[numWheels];
        wheelCoordinates[0] = new Vector3(0.194999993f,0.0680000037f,-0.279000014f);
        wheelCoordinates[1] = new Vector3(-0.194999993f,0.0680000037f,-0.279000014f);
        wheelCoordinates[2] = new Vector3(0.194999993f,0.0680000037f,0.278800011f);
        wheelCoordinates[3] = new Vector3(-0.195899993f,0.0680000037f,0.278800011f);
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // Matrix Resize
        Matrix4x4 resize_wheels  = HW_Transforms.ScaleMat(0.12f, 0.12f, 0.12f);
        // A matrix to move the object
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x,
                                                      displacement.y,
                                                      displacement.z);

        Matrix4x4 spinWheels = HW_Transforms.RotateMat(-160 * Time.time,
                                                       AXIS.X);
        
        // Calculate displacement

        float rotateAngle = Mathf.Atan2(direction.z, direction.x) * Mathf.Rad2Deg - 270;
        Debug.Log(rotateAngle);
        Matrix4x4 rotateObject = HW_Transforms.RotateMat(rotateAngle,
                                                         AXIS.Y);

        // Combine all the matrices into a single one
        // Rotate around a pivot point
        //Matrix4x4 composite = moveObject * rotate * moveOrigin;
        // Roll and move as a wheel
        Matrix4x4 compositeCar = move * rotateObject;

        // Multiply each vertex in the mesh by the composite matrix
        for (int i=0; i<newVertices.Length; i++) {
            Vector4 temp = new Vector4(baseVertices[i].x,
                                       baseVertices[i].y,
                                       baseVertices[i].z,
                                       1);
            newVertices[i] = compositeCar * temp;
        }
        for (int v=0; v<numWheels; v++) {
            for (int a=0; a<newVerticesWheel[v].Length; a++) {
                Vector4 temp = new Vector4(baseVerticesWheel[v][a].x,
                                           baseVerticesWheel[v][a].y,
                                           baseVerticesWheel[v][a].z,
                                           1);

                Matrix4x4 translateWheels = HW_Transforms.TranslationMat(wheelCoordinates[v].x,
                                                                         wheelCoordinates[v].y,
                                                                         wheelCoordinates[v].z);
                Matrix4x4 compositeWheels = move * rotateObject *  translateWheels * spinWheels * resize_wheels;
                newVerticesWheel[v][a] = compositeWheels * temp;
            }
            meshWheel[v].vertices = newVerticesWheel[v];
            meshWheel[v].RecalculateNormals();
            meshWheel[v].RecalculateBounds();
        }

        // Replace the vertices in the mesh
        mesh.vertices = newVertices;
        // Make sure the normals are adapted to the new vertex positions
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();
    }
}
