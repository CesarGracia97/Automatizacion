import { Component } from '@angular/core';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  mensaje: string | null = null; // Mensaje para la vista
  archivos: File[] = []; // Almacenamos los archivos seleccionados

  PROVEEDORES = [ "OSP", "COVENTAS", "SERVICOBRANZA"];
  FORMATO = [ "CUENTA TITAN", "Referencia interna", "DOCUMENTO IDENTIFICACION", "NOMBRE DEL CLIENTE", "TELEFONOS", "CIUDAD", 
    "ESTADO CUENTA", "TIPO CUENTA", "TIPO DE NEGOCIO", "FORMA DE PAGO", "TRANSACCION", "NOM_TRANSACCION", "# FAC PEN CARGA", 
    "# FACTURAS PENDIENTE", "SALDO ORIGINAL VENC", "GESTION COBRANZA TOTAL", "TOTAL A PAGAR VENCIDO", "SALDO ACTUAL", "TOTAL A PAGAR", 
    "MOVIMIENTOS (+)", "MOVIMIENTOS (-)", "TOTAL PAGO", "Valor ajuste", "ESTADO_LIQUIDACION", "LIQ. GC POR VALIDAR", 
    "Gestion OK GC_NO GC", "Fecha pago", "[RESUMEN CONTACTO IVR]", "Fecha IVR", "[RESUMEN CONTACTO LLAMADA]", "Fecha llamada", 
    "[LIQ. TVCABLE]", "CONVENIO", "Respaldo", "CORREO CLIENTE", "EMAIL_CAMPAÑA", "CELULAR CAMPAÑA", "Fecha terminacion", 
    "Empresa", "Dias Vencidos"
  ];

  onFileSelect(event: Event) {
    const files = Array.from((event.target as HTMLInputElement).files || []);
    const nuevosArchivos = this.archivos.concat(files);
    const nombresArchivos = new Set<string>();
    const proveedoresDuplicados = new Set<string>();
    const proveedorArchivoMap: { [proveedor: string]: number } = {};

    for (const archivo of nuevosArchivos) {
      const nombreArchivo = archivo.name;
      if (nombresArchivos.has(nombreArchivo)) {// Verificar duplicados de nombres de archivos
        this.mensaje = `Error: El archivo "${nombreArchivo}" ya está cargado.`;
        return;
      }
      nombresArchivos.add(nombreArchivo);
      for (const proveedor of this.PROVEEDORES) {// Verificar duplicados de proveedores
        if (nombreArchivo.includes(proveedor)) {
          if (!proveedorArchivoMap[proveedor]) {
            proveedorArchivoMap[proveedor] = 1;
          } else {
            proveedorArchivoMap[proveedor]++;
            proveedoresDuplicados.add(proveedor);
          }
        }
      }
    }
    if (proveedoresDuplicados.size > 0) {
      this.mensaje = `Existen archivos del PROVEEDOR ${Array.from(proveedoresDuplicados).join(', ')} duplicados.`;
      return;
    }

    // Validar formato de los archivos
    const errorFormato = this.validarFormato(nuevosArchivos);
    if (errorFormato) {
      this.mensaje = errorFormato;
      return;
    }

    // Si todo está correcto, almacenar los archivos y mostrar éxito
    this.archivos = nuevosArchivos;
    this.mensaje = "Archivos cargados exitosamente.";
  }

  validarFormato(archivos: File[]): string | null {
    for (const archivo of archivos) {
      const reader = new FileReader();

      reader.onload = (e: any) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array', sheetRows: 1  });
        const hoja = workbook.Sheets[workbook.SheetNames[0]];

        if (!hoja) {
          this.mensaje = `El archivo "${archivo.name}" no contiene una hoja válida.`;
          return;
        }

        // Obtener la primera fila como array
        const rango = XLSX.utils.decode_range(hoja['!ref']!);
        const primeraFila: string[] = [];

        const maxColumnas = Math.min(40, rango.e.c + 1);
        for (let columna = rango.s.c; columna < maxColumnas; columna++) {
          const celda = hoja[XLSX.utils.encode_cell({ r: 0, c: columna })];
          if (celda) primeraFila.push(celda.v.toString().trim()); // Eliminar espacios al inicio y al final
        }

        // Validar los títulos contra la lista FORMATO
        for (const titulo of primeraFila) {
          if (!this.FORMATO.includes(titulo)) {
            this.mensaje = `El archivo "${archivo.name}" contiene un título no registrado: "${titulo}".`;
            return;
          }
        }
        this.mensaje = `El archivo "${archivo.name}" ha pasado la validación de formato.`;
      };
      // Leer archivo como array buffer para procesar con XLSX
      reader.readAsArrayBuffer(archivo);
    }
    this.mensaje = "Archivos cargados validados exitosamente.";
    return null; // Si pasa todas las validaciones
  }
}