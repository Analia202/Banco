import { useState } from 'react';
import api from '../services/api';

export default function AuthForm({ onLogin }: { onLogin: (token: string) => void }) {
  const [esRegistro, setEsRegistro] = useState(false);
  const [form, setForm] = useState({
    username: '',
    password: '',
    nombre_completo: '',
    ci: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const res = await api.post('auth/token/login/', {
        username: form.username,
        password: form.password,
      });
      onLogin(res.data.auth_token);
    } catch {
      alert('Login fallido');
    }
  };

  const handleRegistro = async () => {
    try {
      await api.post('auth/users/', {
        username: form.username,
        password: form.password,
        nombre_completo: form.nombre_completo,
        ci: form.ci
      });
      alert('Cuenta creada, ahora inicia sesión');
      setEsRegistro(false);
    } catch {
      alert('No se pudo crear la cuenta');
    }
  };

  return (
    <div>
      <h2>{esRegistro ? 'Crear cuenta bancaria' : 'Iniciar sesión'}</h2>

      {esRegistro && (
        <>
          <input name="nombre_completo" placeholder="Nombre completo" onChange={handleChange} />
          <input name="ci" placeholder="CI" onChange={handleChange} />
        </>
      )}

      <input name="username" placeholder="Usuario" onChange={handleChange} />
      <input name="password" type="password" placeholder="Contraseña" onChange={handleChange} />

      <button onClick={esRegistro ? handleRegistro : handleLogin}>
        {esRegistro ? 'Registrarse' : 'Ingresar'}
      </button>

      <p onClick={() => setEsRegistro(!esRegistro)} style={{ cursor: 'pointer', color: 'blue' }}>
        {esRegistro ? '¿Ya tienes cuenta? Inicia sesión' : '¿No tienes cuenta? Regístrate'}
      </p>
    </div>
  );
}
