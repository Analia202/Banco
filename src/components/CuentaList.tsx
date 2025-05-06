import { useEffect, useState } from 'react';
import api from '../services/api';
import { Cuenta } from '../types';

export default function CuentaList() {
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);

  useEffect(() => {
    api.get('api/mis-cuentas/')
      .then(res => setCuentas(res.data))
      .catch(err => alert("Error al obtener cuentas"));
  }, []);

  return (
    <div>
      <h2>Mis cuentas</h2>
      <ul>
        {cuentas.map(c => (
          <li key={c.id}>N° {c.numero} — Saldo: {c.saldo} Bs</li>
        ))}
      </ul>
    </div>
  );
}