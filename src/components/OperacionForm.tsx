import { useState } from 'react';
import api from '../services/api';

export default function OperacionForm() {
  const [cuentaId, setCuentaId] = useState('');
  const [monto, setMonto] = useState('');
  const [tipo, setTipo] = useState<'ingreso' | 'egreso'>('ingreso');

  const enviar = async () => {
    const endpoint = tipo === 'ingreso' ? 'ingreso/' : 'egreso/';
    try {
      await api.post(`api/${endpoint}`, { cuenta_id: cuentaId, monto });
      alert('Operación realizada');
    } catch (error) {
      alert('Error al realizar la operación');
    }
  };

  return (
    <div>
      <h2>Operación</h2>
      <select onChange={e => setTipo(e.target.value as 'ingreso' | 'egreso')} value={tipo}>
        <option value="ingreso">Ingreso</option>
        <option value="egreso">Egreso</option>
      </select>
      <input placeholder="ID Cuenta" value={cuentaId} onChange={e => setCuentaId(e.target.value)} />
      <input placeholder="Monto" value={monto} onChange={e => setMonto(e.target.value)} />
      <button onClick={enviar}>Enviar</button>
    </div>
  );
}