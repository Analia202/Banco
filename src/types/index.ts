export interface Cuenta {
    id: number;
    numero: string;
    saldo: string;
  }
  
  export interface Movimiento {
    id: number;
    tipo: string;
    monto: string;
    descripcion?: string;
    fecha: string;
  }
  
  export interface Beneficiario {
    id: number;
    nombre: string;
    nro_cuenta: string;
  }
  