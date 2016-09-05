/*
*@file pcap Basado en ejemplo.pcap dado por el ayudante
*           y en el sniffer implementado por tcpdump (http://www.tcpdump.org)
*@brief Programa que permite capturar paquetes, ya sea uno o
*      indefinidos y lo muestra en pantalla
*@author Vilchis Domínguez Miguel Alonso
*@author Bernal Cedillo Enrique Antonio
*@author Velasquez Garzon Angie Daniela
*/

/*++++++++++++++++Compilacion y uso +++++++++++++++++++++++++
*Para instalar libpcap: apt-get install libpcap-dev
*Para compilar el programa la linea de comandos corrrespondiente
*es: gcc ejemplo_pcap.c -o lab -lpcap
*Y como super usuario se ejecuta ./lab
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pcap.h>
#include <arpa/inet.h>
#include "pcap.h"

// Contador global de indice de paquetes
int indice = 0;

/**************************************************************
*@brief Dada un buffer de caracteres (a) y una subcadena (b)
*       regresa verdadero si el buffer inicia con la subcadena
*       regresa falso en otro caso
***************************************************************/
int empiezaCon(const char *a, const char *b){
    if(strncmp(a, b, strlen(b)) == 0)
        return 1;
    return 0;
}

/**************************************************************
*@brief Dado un apuntador de un buffer de caracteres,
*       imprime todo el contenido hasta encontrar el caracter de escape
*       utilizado en TCP para separar los campos y argumentos de los paquetes
***************************************************************/
void imprimeHastaEscape(char *string){
    printf("--) ");
    const u_char *ch;
    ch = string;
    while(isprint(*ch)){
        printf("%c", *ch);
        ch++;
    }
    printf("\n");
}

/**************************************************************
*@brief Dado un buffer de caracteres imprime el contenido de acuerdo
*       al formato requerido para los paquetes de tipo RESPONSE
***************************************************************/
void imprimeResponse(const char *buffer){
    // Status code
    printf("--) Status code: %c%c%c\n", buffer[9], buffer[10], buffer[11]);

    char *str_connection = strstr(buffer, "Connection:");
    if (str_connection == NULL)
        printf("--) Connection: Campo no definido\n");
    else
        imprimeHastaEscape(str_connection);

    char *str_date = strstr(buffer, "Date:");
    if (str_date == NULL)
        printf("--) Date: Campo no definido\n");
    else
        imprimeHastaEscape(str_date);

    char *str_server = strstr(buffer, "Server:");
    if (str_server == NULL)
        printf("--) Server: Campo no definido\n");
    else
        imprimeHastaEscape(str_server);

    char *str_last_modified = strstr(buffer, "Last-Modified:");
    if (str_last_modified == NULL)
        printf("--) Last-Modified: Campo no definido\n");
    else
        imprimeHastaEscape(str_last_modified);

    char *str_content_length = strstr(buffer, "Content-Length:");
    if (str_content_length == NULL)
        printf("--) Content-Length: Campo no definido\n");
    else
        imprimeHastaEscape(str_content_length);

    char *str_content_type = strstr(buffer, "Content-Type:");
    if (str_content_type == NULL)
        printf("--) Content-Type: Campo no definido\n");
    else
        imprimeHastaEscape(str_content_type);
}

/**************************************************************
*@brief Dado un buffer de caracteres imprime el contenido de acuerdo
*       al formato requerido para los paquetes de tipo REQUEST
***************************************************************/
void imprimeRequest(const char *buffer){
    if(empiezaCon(buffer, "POST"))
        printf("--) Method: POST\n");

    if(empiezaCon(buffer, "GET"))
        printf("--) Method: GET\n");

    if(empiezaCon(buffer, "HEAD"))
        printf("--) Method: HEAD\n");

    if(empiezaCon(buffer, "OPTIONS"))
        printf("--) Method: OPTIONS\n");

    if(empiezaCon(buffer, "PUT"))
        printf("--) Method: PUT\n");

    if(empiezaCon(buffer, "DELETE"))
        printf("--) Method: DELETE\n");

    if(empiezaCon(buffer, "TRACE"))
        printf("--) Method: TRACE\n");

    if(empiezaCon(buffer, "CONNECT"))
        printf("--) Method: CONNECT\n");

    char *str_host = strstr(buffer, "Host:");
    if (str_host == NULL)
        printf("--) Host: Campo no definido\n");
    else
        imprimeHastaEscape(str_host);

    char *str_user_agent = strstr(buffer, "User-Agent:");
    if (str_user_agent == NULL)
        printf("--) User-Agent: Campo no definido\n");
    else
        imprimeHastaEscape(str_user_agent);

    char *str_connection = strstr(buffer, "Connection:");
    if (str_connection == NULL)
        printf("--) Connection: Campo no definido\n");
    else
        imprimeHastaEscape(str_connection);

    char *str_accept_language = strstr(buffer, "Accept-Language:");
    if (str_accept_language == NULL)
        printf("--) Accept-Language: Campo no definido\n");
    else
        imprimeHastaEscape(str_accept_language);
}

/**************************************************************
*@brief Funcion que es llamada cada vez que se detecta un paquete en la captura,
*       Utilizando las estructuras auxiliares definidas en pcap.h
*       Obtiene la longitud del paquete, muestra la IP fuente y destino,
*       En caso de que el paquete cumpla el protocolo TCP, investiga la cabecera TCP,
*       Para mostrar los datos requeridos de Request y Response HTTP
***************************************************************/
void procesarPaquete(u_char *args, const struct pcap_pkthdr *header, const u_char *paquete){
    // Informacion de cabecera del paquete
    indice++;
    //printf("Longitud del mensaje en total: %d\n", header->len);

    // Procesando el header de IP
    const struct ip_header *ip;
    int size_ip;
    ip = (struct ip_header*) (paquete + TAM_ETHERNET);
    size_ip = IP_HL(ip)*4;
    if(size_ip < 20){
        //printf("x) La longitud del header IP es invalida: %u bytes\n\n", size_ip);
        return;
    }

    // Remitente y destinatario (direcciones IP)
    //printf("(SRC: %p) %s -> (DEST: %p) %s \n", (void*)&(*ip).ip_src, inet_ntoa(ip->ip_src), (void*)&(*ip).ip_dst, inet_ntoa(ip->ip_dst));

    // En caso de que el paquete sea del protocolo TCP se continua con el proceso
    if(ip->ip_p == IPPROTO_TCP){
        const struct sniff_tcp *tcp;            /* TCP header */
        int size_tcp;
        const char *payload;                    /* Packet payload */
        int size_payload;
        char* nombre;
        nombre = "TCP";
        /* Parsing del header tcp */
        tcp = (struct sniff_tcp*) (paquete + TAM_ETHERNET + size_ip);
        size_tcp = TH_OFF(tcp)*4;
        if(size_tcp < 20){
            //printf("x) La longitud del header TCP es invalida: %u bytes\n\n", size_tcp);
            return;
        }
        // Proceso del segmento de informacion del header TPC
        payload = (u_char *) (paquete + TAM_ETHERNET + size_ip + size_tcp);
        size_payload = ntohs(ip->ip_len) - (size_ip + size_tcp);
        // Mostrando informacion de cabecera TCP
        if (size_payload > 0){
            // Si comienza con algunas de las siguientes palabras reservadas, el paquete nos interesa
            if( empiezaCon(payload, "HTTP") || empiezaCon(payload, "POST") || empiezaCon(payload, "GET") ||
                empiezaCon(payload, "HEAD") || empiezaCon(payload, "OPTIONS") || empiezaCon(payload, "PUT") ||
                empiezaCon(payload, "DELETE") || empiezaCon(payload, "TRACE") || empiezaCon(payload, "CONNECT")){
                printf("(--------------- INDICE PAQUETE OBTENIDO (%d) ----------------)\n", indice);
                printf("--) Protocolo: %x (%s)\n", ip->ip_p, nombre);
                printf("    Puerto remitente: %d\n", ntohs(tcp->th_sport));
                printf("    Puerto destino: %d\n", ntohs(tcp->th_dport));
                if (empiezaCon(payload, "HTTP")){
                    //Muestra la informacion de un response
                    printf("-) RESPONSE\n");
                    imprimeResponse(payload);
                }else{
                    //Muestra la informacion de un request
                    printf("-) REQUEST\n");
                    imprimeRequest(payload);
                }
            printf("X--------------- PAQUETE PROCESADO ---------------X\n\n");
            }
        }
        /* Fin del parsing del header TCP */
    }else{
        // Protocolo no relacionado a HTTP
        //printf("--) El paquete (%d) utilza un protocolo no relacionado con HTTP\n", indice);
        //printf("    Numero identificador del protocolo: %d\n\n", ip->ip_p);
        return;
    }
 }

/**************************************************************
*@brief Dada una captura y el nombre del dispositivo,
*       itera sobre cada paquete dentro de la captura indefinidamente, 
*       o hasta que ocurra un error
***************************************************************/
int leerPaquetes(pcap_t* captura, char* dev){
    //Iteramos sobre los paquetes utilizando la funcion auxiliar para cada uno (-1 = Lectura indefinida)
    pcap_loop(captura, -1, procesarPaquete, NULL);
    // Seria bueno ver como llegar a este close, debido a que pcap_loop es "infinito"
    pcap_close(captura);
    return EXIT_SUCCESS;
}

/**************************************************************
 *@brief Rutina que muestra los dispositivos de red que pueden ser escuchados,
         y permite elegir uno para realizar una captura y ser analizado
 ***************************************************************/
int capturaDispositivo(){
    // Obtenemos la lista de interfaces de red que pueden abrirse
    char ebuf[PCAP_ERRBUF_SIZE];
    pcap_if_t* deviceList;
    if (pcap_findalldevs(&deviceList,ebuf) == -1){
        printf("Al obtener listado de dispositivos. ERROR: %s\n", ebuf);
        return EXIT_FAILURE;
    }else{
        printf("--) Lista de interfaces de red:\n");
    }
    // Iteramos la lista de dispositivos disponibles
    int i = 0;
    while(deviceList->next != NULL ) {
        printf("  %d.- %s\n", i+1, (deviceList->name));
        deviceList = deviceList->next;
        i++;
    }
    //Obtenemos la interfaz de red tecleada por el usuario    
    printf("--) Teclea el NOMBRE de la interfaz de red con la que deseas interactuar:\n");
    char dev[256];
    fgets(dev, sizeof dev, stdin);
    char *pos;
    if ((pos = strchr(dev, '\n')) != NULL)
        *pos = '\0';
    //Si la cadena con el nombre del dispositivo de red no es válida, no continuamos
    if(dev == NULL){
        printf("x) Nombre de dispositivo no valido. ERROR\n");
        return EXIT_FAILURE;
    }
    //Imprimimos el dispositivo de red a capturar
    printf("--) Capturaremos del dispositivo: %s\n\n", dev);
    //Abrimos la interfaz de red
    pcap_t *captura;
    captura = pcap_open_live(dev, BUFSIZ, 1, 1000, ebuf);
    //Si la captura realizada no fue exitosa salimos del programa
    if(captura == NULL) {
        printf("x) En captura. ERROR: %s\n", ebuf);
        return EXIT_FAILURE;
    }
    // Aplicamos filtro para unicamente actuar en paquetes http    
    bpf_u_int32 mask; //Netmask del sniffer
    bpf_u_int32 net;  //IP del sniffer
    if (pcap_lookupnet(dev, &net, &mask, ebuf) == -1){
        printf("Error al configurar filtro: %s\n", ebuf);
        return EXIT_FAILURE;
    }
    struct bpf_program fp;
    // En el puerto 80 ocurre el intercambio de paquetes http a traves de tcp
    //pcap_compile(captura, &fp, "tcp port 80", 0, net);
    pcap_compile(captura, &fp, "tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)", 0, net);
    pcap_setfilter(captura, &fp);

    // Con la captura lista procedemos a leer sus paquetes
    leerPaquetes(captura, dev);
 }

/**************************************************************
*@brief Rutina en la que se recibe el nombre del archivo,
        y realiza la captura con los datos que contiene
***************************************************************/
int leeCaptura(){
    char ebuf[PCAP_ERRBUF_SIZE];
    printf("--) Teclea el NOMBRE del archivo que contiene la captura a analizar.\n");
    char dev[256];
    fgets(dev, sizeof dev, stdin);
    char *pos;
    if ((pos = strchr(dev, '\n')) != NULL)
        *pos = '\0';
    //Si la cadena con el nombre del archivo no es válida, termina la ejecucion
    if(dev == NULL){
        printf("x) Nombre de dispositivo no valido. ERROR\n");
        return EXIT_FAILURE;
    }
    //Imprimimos el nombre del archivo con la captura
    printf("--) Leyendo archivo: %s\n\n", dev);
    //Abrimos la captura a partir del archivo
    pcap_t *captura;
    captura = pcap_open_offline(dev, ebuf);
    //Si la captura realizada no fue exitosa salimos del programa
    if(captura == NULL) {
        printf("x) En captura. ERROR: %s\n", ebuf);
        return EXIT_FAILURE;
    }
    // Con la captura lista procedemos a leer sus paquetes
    leerPaquetes(captura, dev);
}

/**************************************************************
*@brief Rutina que limpia la entrada standard
***************************************************************/
int clean_stdin(){
    while (getchar()!='\n');
    return 1;
}

/**************************************************************
*@brief Funcion principal del programa, permite eligir el
*       modo de trabajo
***************************************************************/
int main () {
    // Capturamos respuesta y continuamos a hacer lo correspondiente a la opcion elegida
    int entrada;
    char c;
    printf("--) Elige el modo en el que se trabajara, tecleando el NUMERO:\n");
    do{
        printf("  (1) Escucha indefinida\n  (2) Lectura de captura\n");
    }while(((scanf("%d%c", &entrada, &c)!=2 || c!='\n') && clean_stdin()) || entrada<1 || entrada>2);

    if (entrada == 1){
        // Escucha indefinida
        capturaDispositivo();
    }else{
        // Lectura de captura
        leeCaptura();
    }   
    return 0;
}