import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const COLORS = ['#FF8042', '#0088FE']; // Colores para Pendiente y Resuelto

const DashboardChart = ({ municipioId }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const url = municipioId
      ? `http://localhost:5000/api/dashboard/estatus?municipio_id=${municipioId}`
      : 'http://localhost:5000/api/dashboard/estatus';

    fetch(url)
      .then(res => res.json())
      .then(json => {
        const chartData = [
          { name: 'Pendiente', value: json.Pendiente || 0 },
          { name: 'Resuelto', value: json.Resuelto || 0 }
        ];
        setData(chartData);
      });
  }, [municipioId]);

  return (
    <div>
      <h2 className="text-lg font-bold mb-2">Estatus de Turnos</h2>
      <PieChart width={300} height={300}>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={90}
          dataKey="value"
          label
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default DashboardChart;
