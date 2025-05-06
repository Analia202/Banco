import { useEffect, useState } from 'react';
import api from '../services/api';
import { Beneficiario } from '../types';

export default function BeneficiarioForm() {
  const [beneficiarios, setBeneficiarios] = useState<Beneficiario[]>([]);
  const [nombre, setNombre] = useState('');
  const [nroCuenta, setNroCuenta] = useState('');

  const cargar = () => {
    api.get('api/beneficiarios/').then(res => setBeneficiarios(res.data));
  };

  useEffect(cargar, []);

  const agregar = () => {
    api.post('api/beneficiarios/', { nombre, nro_cuenta: nroCuenta })
      .then(cargar);
  };

  return (
    <div>
      <h2>Beneficiarios</h2>
      <input placeholder="Nombre" value={nombre} onChange={e => setNombre(e.target.value)} />
      <input placeholder="Nro Cuenta" value={nroCuenta} onChange={e => setNroCuenta(e.target.value)} />
      <button onClick={agregar}>Agregar</button>
      <ul>
        {beneficiarios.map(b => (
          <li key={b.id}>{b.nombre} - {b.nro_cuenta}</li>
        ))}
      </ul>
    </div>
  );
}
