import { useEffect, useState } from "react";

function MunicipiosCrud() {
  const [municipios, setMunicipios] = useState([]);
  const [nombre, setNombre] = useState("");
  const [editId, setEditId] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [municipioSeleccionado, setMunicipioSeleccionado] = useState(""); // Estado para manejar el municipio seleccionado

  const API_URL = "http://localhost:5000/api/municipios/";

  useEffect(() => {
    cargarMunicipios();
  }, []);

  const cargarMunicipios = async () => {
    const res = await fetch(API_URL);
    const data = await res.json();
    setMunicipios(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nombre.trim()) return;

    const datos = { nombre };

    try {
      let res;
      if (editId) {
        res = await fetch(`${API_URL}/${editId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(datos),
        });
      } else {
        res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(datos),
        });
      }

      const result = await res.json();
      if (res.ok) {
        setMensaje("Guardado correctamente");
        setNombre("");
        setEditId(null);
        cargarMunicipios();
      } else {
        setMensaje(result.error || "Error en la operación");
      }
    } catch (error) {
      console.error("Error:", error);
      setMensaje("Error de conexión");
    }
  };

  const editar = (municipio) => {
    setNombre(municipio.nombre);
    setEditId(municipio.id);
    setMunicipioSeleccionado(municipio.id); // Se selecciona el municipio a editar
  };

  const eliminar = async (id) => {
    if (!window.confirm("¿Eliminar este municipio?")) return;
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarMunicipios();
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto" }}>
      <h2>{editId ? "Editar Municipio" : "Agregar Municipio"}</h2>
      <form onSubmit={handleSubmit}>
        {/* Aquí hay un select para elegir un municipio */}
        <select
          value={municipioSeleccionado}
          onChange={(e) => setMunicipioSeleccionado(e.target.value)}
          required
        >
          <option value="">Selecciona un Municipio</option>
          {municipios.map((m) => (
            <option key={m.id} value={m.id}>
              {m.nombre}
            </option>
          ))}
        </select>
        
        <input
          type="text"
          placeholder="Nombre del municipio"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
          style={{ padding: 8, width: "80%", marginRight: 8 }}
        />
        <button type="submit">{editId ? "Actualizar" : "Guardar"}</button>
        {editId && (
          <button type="button" onClick={() => { setEditId(null); setNombre(""); }}>
            Cancelar
          </button>
        )}
      </form>
      <p>{mensaje}</p>

      <h3>Lista de Municipios</h3>
      <table border="1" cellPadding="8" width="100%">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {municipios.length === 0 ? (
            <tr>
              <td colSpan="3">No hay municipios registrados</td>
            </tr>
          ) : (
            municipios.map((m) => (
              <tr key={m.id}>
                <td>{m.id}</td>
                <td>{m.nombre}</td>
                <td>
                  <button onClick={() => editar(m)}>Editar</button>
                  <button onClick={() => eliminar(m.id)}>Eliminar</button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default MunicipiosCrud;
