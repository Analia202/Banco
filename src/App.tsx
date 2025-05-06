import { useState } from 'react';
import LoginForm from './components/LoginForm';
import CuentaList from './components/CuentaList';
import OperacionForm from './components/OperacionForm';
import BeneficiarioForm from './components/BeneficiarioForm';
import api from './services/api';

function App() {
  const [token, setToken] = useState('');

  if (!token) {
    return <LoginForm onLogin={(t) => {
      api.defaults.headers.common['Authorization'] = `Token ${t}`;
      setToken(t);
    }} />;
  }

  return (
    <div>
      <h1>Banco</h1>
      <CuentaList />
      <OperacionForm />
      <BeneficiarioForm />
    </div>
  );
}

export default App;
