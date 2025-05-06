import { useState } from 'react';
import api from '../services/api';

export default function LoginForm({ onLogin }: { onLogin: (token: string) => void }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const login = async () => {
    try {
      const res = await api.post('auth/token/login/', { username, password });
      onLogin(res.data.auth_token);
    } catch (error) {
      alert('Usuario o contraseña incorrectos');
    }
  };

  return (
    <div>
      <h2>Iniciar sesión</h2>
      <input placeholder="Usuario" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={login}>Ingresar</button>
    </div>
  );
}
