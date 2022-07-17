## INTRO

L'applicazione e' stata sviluppata co il seguente stack: 
* Flask per il backend
* Postgres per il database
* Redis come message-broker di task asincroni
* Celery come consumer dei task asincroni

## Database

Il modello di dati possibilmente variabile si sarebbe potuto adattare bene per un database NoSQL, comunque, per evitare un modello piatto, e' stato scelto un DB relazione.

I dati sono stati modellati con 3 tabelle
* Restaurant
* Address
* Info

le ultime due in relazione 1 a 1 con la prima.

## Avviare l'applicazione

Per avviare l'applicazione, dalla cartella root bisogna lanciare il comando


```shell
docker-compose up
```

Una volta che tutti i container sono avviati, l'applicazione web asacolta al seguente indirizzo:
```
http://localhost:5000
```
## API

Sono esposti i seguenti endpoint:

* Endpoint di test

```
GET http://localhost:5000
```
___________
* Endpoint di caricamento dei dati

Accetta come body sia il file json (`/src/test_data/test.json`) che il suo contenuto in formato 'raw'.

```
POST http://localhost:5000/add
```

Questo endpoint gestisce il caricamento in modo asincrono, restituira' quindi l'id del task che sta eseguendo il caricamento nel formato
```json
{
    "id": "870e72c0-4ae0-48cd-bb52-654c2a10244f"
}
```
___________

* Endpoint per interrogare lo stato del task di caricamento

```
GET http://localhost:5000/task_status/<task_id>
```
restituira' la seguente risposta dove le chiavi `state` e `result` cambieranno a seconda che il task sia ancora in corso, sia completato con successo o sia fallito. Ad esempio in caso dicompletamento con successo mostrera' una risposta del tipo:
```json
{
    "result": {
        "added": 500,
        "total": 500
    },
    "state": "SUCCESS"
}
```
NB. si e' supposto che i Ristoranti fossero univoci nella combinazione `nome - tipo`, per cui inserimenti successivi di dati gia' presenti non verranno considerati.

Lo stato dei task e' anche visulizzabile tramite la dashbord di `flower`  (https://flower.readthedocs.io/en/latest/) esposto alla porta ` http://localhost:5555`

___________

* Endpoint per cancellare un Ristorante tramite id

```
DELETE http://localhost:5000/del/<id>
```
___________
* Endpoint di visualizzazione dei dati

E' stata usata la libreria Flask-Admin per fornire una veloce visualizzazione deidati salvati a DB, raggiungibile al seguente endpoint

```
POST http://localhost:5000/admin
```

## TEST VELOCE DELL'APPLICAZIONE
E' possibile testare l'applicazione da riga di comando avviando, dalla root del progetto, i seguenti comandi

Questo comndo chiama l'endpoint di caricamento
```sh
sh run_program
```
___
Con questo comando invece, passando come argomento il `<task_id>` restituito dal comando precedente, si puo' visualizzare lo stato del task
```sh
sh result_by_job_id <task_id>
```
___________
Per visualizzare i risultati
```
POST http://localhost:5000/admin
```

