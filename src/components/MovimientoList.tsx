import { useEffect, useState } from 'react';
import api from '../services/api';
import { Movimiento } from '../types';

export default function MovimientoList({ cuentaId }: { cuentaId: number }) {
  const [movimientos, setMovimientos] = useState<Movimiento[]>([]);

  useEffect(() => {
    api.get(`api/movimientos/${cuentaId}/`)
      .then(res => setMovimientos(res.data))
      .catch(err => alert("Error al obtener movimientos"));
  }, [cuentaId]);

  return (
    <div>
      <h3>Movimientos</h3>
      <ul>
        {movimientos.map(m => (
          <li key={m.id}>{m.tipo} - {m.monto} Bs - {new Date(m.fecha).toLocaleDateString()}</li>
        ))}
      </ul>
    </div>
  );
}