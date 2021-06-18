import fdb
import configparser
import imapclient
import ssl
import smtplib
import time
import sys

print("System automatycznej odpowiedzi na zapytania o saldo działkowców. Wersja 0.1")
print("Copyright (C) 2021 Filip Napierała")
print("Data kompilacji 18.06.2021r.")
print("--------------------------------------------------------------------------------------------------------")
print("Niniejszy program jest wolnym oprogramowaniem - możesz go rozpowszechniać dalej i/lub modyfikować ")
print("na warunkach Powszechnej Licencji Publicznej GNU")
print("wydanej przez Fundację Wolnego Oprogramowania, według wersji 3 tej Licencji lub dowolnej z późniejszych wersji.")
print("Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on użyteczny - jednak BEZ ŻADNEJ GWARANCJI,")
print("nawet domyślnej gwarancji PRZYDATNOŚCI HANDLOWEJ,")
print("albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ. Bliższe informacje na ten temat można uzyskać z")
print("Powszechnej Licencji Publicznej GNU.")
print("Powszechna Licencja Publiczna GNU powinna zostać ci dostarczona razem z tym programem")
print("--------------------------------------------------------------------------------------------------------")
print("Program powinien być uruchamiany na serwerze")
print("Proszę sprawdzić plik config.txt pod kątem zgodności danych domyślnych z tymi na Państwa Ogrodzie")
print("Potencjalne aktualizacje programu będą dostępne pod adresem: www.github.com/filnap/RodMailBot")

config = "config.txt"
parser = configparser.ConfigParser()
parser.read('config.txt')

# Database
filepath = parser['BASIC']['filepath']
database = parser['BASIC']['database']
user = parser['BASIC']['user']
password = parser['BASIC']['password']
# E-mail
port = parser['EMAIL']['port']  # For starttls
smtp_server = parser['EMAIL']['smtp_server']
imap_server = parser['EMAIL']['imap_server']
sender_email = parser['EMAIL']['sender_email']
password_email = parser['EMAIL']['password_email']
# Naliczenia
naliczenie1 = parser['NALICZENIA']['naliczenie1']
naliczenie2 = parser['NALICZENIA']['naliczenie2']
naliczenie3 = parser['NALICZENIA']['naliczenie3']
naliczenie4 = parser['NALICZENIA']['naliczenie4']
naliczenie5 = parser['NALICZENIA']['naliczenie5']
naliczenie6 = parser['NALICZENIA']['naliczenie6']
naliczenie7 = parser['NALICZENIA']['naliczenie7']
naliczenie8 = parser['NALICZENIA']['naliczenie8']
naliczenie9 = parser['NALICZENIA']['naliczenie9']
naliczenie10 = parser['NALICZENIA']['naliczenie10']
naliczenie11 = parser['NALICZENIA']['naliczenie11']
naliczenie12 = parser['NALICZENIA']['naliczenie12']
naliczenie13 = parser['NALICZENIA']['naliczenie13']
naliczenie14 = parser['NALICZENIA']['naliczenie14']
naliczenie15 = parser['NALICZENIA']['naliczenie15']
naliczenie16 = parser['NALICZENIA']['naliczenie16']
naliczenie17 = parser['NALICZENIA']['naliczenie17']
naliczenie18 = parser['NALICZENIA']['naliczenie18']
naliczenie19 = parser['NALICZENIA']['naliczenie19']
naliczenie20 = parser['NALICZENIA']['naliczenie20']
naliczenie21 = parser['NALICZENIA']['naliczenie21']
naliczenie22 = parser['NALICZENIA']['naliczenie22']
naliczenie23 = parser['NALICZENIA']['naliczenie23']
naliczenie24 = parser['NALICZENIA']['naliczenie24']
naliczenie25 = parser['NALICZENIA']['naliczenie25']
naliczenie26 = parser['NALICZENIA']['naliczenie26']
naliczenie27 = parser['NALICZENIA']['naliczenie27']
naliczenie28 = parser['NALICZENIA']['naliczenie28']
naliczenie29 = parser['NALICZENIA']['naliczenie29']
naliczenie30 = parser['NALICZENIA']['naliczenie30']
naliczenie31 = parser['NALICZENIA']['naliczenie31']
naliczenie32 = parser['NALICZENIA']['naliczenie32']
naliczenie33 = parser['NALICZENIA']['naliczenie33']
naliczenie34 = parser['NALICZENIA']['naliczenie34']
naliczenie35 = parser['NALICZENIA']['naliczenie35']
naliczenie36 = parser['NALICZENIA']['naliczenie36']
naliczenie37 = parser['NALICZENIA']['naliczenie37']

print("Wszystkie dane wpisane prawidłowo")

imap = imapclient.IMAPClient(imap_server)
imap.login(sender_email, password_email)
# foldery = imap.list_folders()
# print(foldery)
while(True):
    imap.select_folder('INBOX')

    incomingmessage = imap.search(['UNSEEN'])
    print("Lista nieodczytanych wiadomości e-mail")
    # TODO: Sprawdzenie, czy działka nie ma bana na maile, zrobić o bazę DGCS!

    for msgid, data in imap.fetch(incomingmessage, ['ENVELOPE']).items():
        envelope = data[b'ENVELOPE']

        print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))
        if envelope.subject.decode() == "#BOT":
            # TODO: Sprawdzenie, czy dotarł mail z tematem #BOT

            print("BOT!")
            senderraw = envelope.from_[0]
            sender = senderraw[2] + b'@' + senderraw[3]
            print("mail nadawcy:")
            print(sender.decode("utf-8"))
            rawmsgs = imap.fetch(msgid, ['BODY[]'])
            # print(rawmsgs)
            con = fdb.connect(database=database, user=user, password=password)
            cur = con.cursor()
            # Main loop
            cur.execute("SELECT IDSIKONTR FROM SIKONTR WHERE EMAIL='%s' " % str(sender.decode("utf-8")))
            idsimailrawraw = cur.fetchall()
            if len(idsimailrawraw) == 1:  # Checking if mail is in database

                idsimail = idsimailrawraw[0][0]

                cur.execute("SELECT IDDZIALKI FROM \"@PZD_RELDZIALKISIKONTR\" WHERE IDSIKONTRWLA='%s' " % str(idsimail))
                iddzialkilist = cur.fetchall()
                iddzialkituple = iddzialkilist[0]
                iddzialki = iddzialkituple[0]
                print("id dzialki:")
                print(iddzialki)

                cur.execute("SELECT NUMERDZIALKI FROM \"@PZD_DZIALKI\" WHERE IDDZIALKI='%s' " % iddzialki)
                nrdzialkilist = cur.fetchall()
                nrdzialkituple = nrdzialkilist[0]
                nrdzialki = nrdzialkituple[0]
                print("Numer dzialki:")
                print(nrdzialki)

                # TODO: Sprawdzenie czy nr działki jest zgodny z mailem właściciela
                L = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                cur.execute("SELECT IDNALICZENIA FROM \"@PZD_NALICZENIA\" WHERE IDDZIALKI='%s'" % iddzialki)
                idnaliczenia = cur.fetchall()

                kwotanaliczen = 0

                i = 0
                j = 0
                KwotaOplat = 0

                for i in range(len(idnaliczenia)):

                    jednoid = idnaliczenia[i]
                    jednoidnal = jednoid[0]
                    cur.execute("SELECT KWOTA FROM \"@PZD_NALICZENIAPOZ\" WHERE IDNALICZENIA='%s'" % jednoidnal)
                    kwotalista = cur.fetchall()

                    # accrual calculation stops here !!!

                    # --------------------------------------------------------------------

                    # checking accrual category
                    cur.execute("SELECT IDSLOOPLATY FROM \"@PZD_NALICZENIAPOZ\" WHERE IDNALICZENIA='%s'" % jednoidnal)
                    idsioplaty = cur.fetchall()
                    # print("IDOPLATY:")
                    # print(idsioplaty)

                    # left to pay check
                    cur.execute("SELECT IDZOBOWIAZANIAKONTR FROM \"@PZD_NALICZENIAPOZ\" WHERE IDNALICZENIA='%s'" % jednoidnal)
                    IDZOBOWIAZANIAKONTR = cur.fetchall()

                    # Weird section
                    for a in range(len(IDZOBOWIAZANIAKONTR)):
                        idzobpierw = IDZOBOWIAZANIAKONTR[a]
                        idzobdrug = idzobpierw[0]
                        # print("idzobowikontr")
                        # print(idzobdrug)
                        cur.execute(
                            "SELECT POZOSTALA_ZALEGLOSC FROM \"@ZAPL_ZOBOWIAZANIAKONTR\" WHERE IDZOBOWIAZANIAKONTR='%s'" % (
                                idzobdrug))
                        pozostalo = cur.fetchall()

                        for l in range(len(pozostalo)):
                            pozostalojeden = pozostalo[l]
                            pozostalodwa = pozostalojeden[0]

                            if pozostalodwa != 0:
                                indeks = idsioplaty[a]
                                indekss = indeks[0]
                                if str(indekss) == "None":
                                    indekss = 38

                                opnalist = L[int(indekss)]
                                L[indekss] = opnalist + pozostalodwa
                            l = l + 1
                        a = a + 1

                        # done
                        # --------------------------------------------------------------------------------------------------
                        # returning to accrual calculation
                    for j in range(len(kwotalista)):
                        kwotatuple = kwotalista[j]
                        kwota = kwotatuple[0]
                        kwotanaliczen = kwotanaliczen + kwota
                        j = j + 1

                    i = i + 1

                    # Payment and email section
                # Finding ID for owners
                cur.execute("SELECT IDSIKONTRWLA FROM \"@PZD_RELDZIALKISIKONTR\" WHERE IDDZIALKI='%s'" % iddzialki)
                idsikontrwlarawWLAS = cur.fetchall()
                # Getting owner's e-mail adress
                idaktualnegoraw = idsikontrwlarawWLAS[len(idsikontrwlarawWLAS) - 1]
                idaktualnego = idaktualnegoraw[0]
                cur.execute("SELECT EMAIL FROM SIKONTR WHERE IDSIKONTR='%s'" % idaktualnego)
                emailrawraw = cur.fetchall()
                emailraw = emailrawraw[0]
                email = emailraw[0]
                # print("email:")
                # print(email)

                # Finding ID for co-owners
                cur.execute("SELECT IDSIKONTRMALZ FROM \"@PZD_RELDZIALKISIKONTR\" WHERE IDDZIALKI='%s'" % iddzialki)
                idsikontrwlarawMALZ = cur.fetchall()

                # Joining owners and co-owners ID lists together
                idsikontrwlarawWLAS.extend(idsikontrwlarawMALZ)
                idsikontrwlaraw = idsikontrwlarawWLAS

                # print(idsikontrwlaraw)
                # To remove duplicates
                idsikontrwla = list(dict.fromkeys(idsikontrwlaraw))
                # print(idsikontrwla)
                for l in range(len(idsikontrwla)):
                    idsikontrwlaJed = idsikontrwla[l]
                    idsikontrwlaDwa = idsikontrwlaJed[0]
                    l = l + 1

                    if idsikontrwlaDwa is not None:
                        # print("ID kontrachenta: " + str(idsikontrwlaDwa))
                        cur.execute("SELECT INDEKSKONTR FROM \"SIKONTR\" WHERE IDSIKONTR='%s'" % idsikontrwlaDwa)
                        indekskontr = cur.fetchall()
                        indekskontr = indekskontr[0]
                        indekskontr = indekskontr[0]
                        # print(indekskontr)
                        # KP and KW
                        cur.execute("SELECT KWOTA FROM \"DOKUMENTYKASOWE\" WHERE INDEKSKONTR ='%s'" % indekskontr)
                        ZbiorczeOplaty = cur.fetchall()
                        # print(ZbiorczeOplaty)

                        k = 0
                        for k in range(len(ZbiorczeOplaty)):
                            OplataJeden = ZbiorczeOplaty[k]
                            KwotaOplatyJeden = OplataJeden[0]
                            KwotaOplat = KwotaOplat + KwotaOplatyJeden
                            k = k + 1
                        # print("Kwota opłat: " + str(KwotaOplat))
                        # Bank statements
                        cur.execute("SELECT KWOTA FROM \"@WYCIAGI_WYC_POZ\" WHERE INDEKSKONTR ='%s'" % indekskontr)
                        Wyciagi = cur.fetchall()

                        m = 0
                        for m in range(len(Wyciagi)):
                            OplataJeden = Wyciagi[m]
                            KwotaOplatyJeden = OplataJeden[0]
                            # print("Kwota z wyciągu:" + str(KwotaOplatyJeden))
                            KwotaOplat = KwotaOplat + KwotaOplatyJeden
                            m = m + 1

                Saldo = kwotanaliczen - KwotaOplat
                # print("Saldo:" + str(Saldo))
                # L[42] = kwotanaliczen
                # L[43] = KwotaOplat
                # L[44] = Saldo

                header = [naliczenie1, naliczenie2, naliczenie3, naliczenie4, naliczenie5, naliczenie6, naliczenie7, naliczenie8, naliczenie9, naliczenie10, naliczenie11, naliczenie12,
                          naliczenie13,
                          naliczenie14, naliczenie15, naliczenie16, naliczenie17, naliczenie18, naliczenie19, naliczenie20, naliczenie21, naliczenie22, naliczenie23, naliczenie24,
                          naliczenie25,
                          naliczenie26, naliczenie27, naliczenie28, naliczenie29, naliczenie30, naliczenie31, naliczenie32, naliczenie33, naliczenie34, naliczenie35, naliczenie36,
                          naliczenie37, "inne", "inne", "inne", "inne", "inne", "inne", "inne", "inne"]

                sendlist = []
                for x in range(len(header)):
                    if L[x] != 0:
                        # print(header[x-1]+": " + str(L[x]) + "PLN") #Uwaga na x-1!
                        sendlist.append("\n" + header[x - 1] + ": " + str(L[x]) + "PLN")
                # print("Kwota zerowa")

                #DATAWYCIĄGU
                cur.execute("SELECT DATA FROM \"@WYCIAGI_WYCIAG\"")
                datawyciagulist = cur.fetchall()
                datawyciagu = datawyciagulist[len(datawyciagulist) - 1][0]

                #STANLICZNIKA
                cur.execute("SELECT IDLICZNIK FROM \"@PZD_RELLICZNIKDZIALKI\" WHERE IDDZIALKI='%s' " % iddzialki)
                idlicznikraw = cur.fetchall()
                idlicznik = idlicznikraw[0][0]
                cur.execute("SELECT DATAODCZYTU FROM \"@PZD_LICZNIKODCZYT\" WHERE IDLICZNIK='%s' " % idlicznik)
                datalicznikraw = cur.fetchall()
                datalicznik = datalicznikraw[len(datalicznikraw) - 1][0]
                print(datalicznik)
                cur.execute("SELECT STANLICZNIKA FROM \"@PZD_LICZNIKODCZYT\" WHERE IDLICZNIK='%s' " % idlicznik)
                stanlicznikraw = cur.fetchall()
                stanlicznik = stanlicznikraw[len(stanlicznikraw) - 1][0]
                print(stanlicznik)


                sendstring = ''.join(map(str, sendlist))
                # print(sendstring)
                message = """Subject: Informacje dla działki nr {nrdzialki} \n
                
                Dzień dobry,
                Odpowiadam na zgłoszenie z dnia {data}.\n
                Adres e-mail {sender} zgodny z bazą.
                Informuje, że na działce nr {nrdzialki} widoczne są następujące zaległości: \n
               {sendstring}\n
                Ostatni znany stan licznika energii elektrycznej dla działki nr {nrdzialki} wynosił {stanlicznik} kWh odczytano dnia {datalicznik}
                Data najnowszego wyciągu bankowego wprowadzonego do systemu to: {datawyciagu} \n
                Z wyrazami szacunku
                BOT ROD KONINKO """.format(nrdzialki=nrdzialki, sender=sender.decode("utf-8"), data=envelope.date, sendstring=sendstring, datawyciagu=datawyciagu,
                                           datalicznik=datalicznik, stanlicznik=stanlicznik)

                # print(message)

                # TODO: Stworzyć program wysyłający maila
                # TODO: Dodać stan ostatniego odczytu + data odczytu
                # TODO: Dodać datę ostatniego wyciągu + opcjonalnie kwotę ostatniej wpłaty
                con.close()
                # Sending an e-mail message
                print("Rozpoczynam wysyłkę")
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.ehlo()  # Can be omitted
                server.login(sender_email, password_email)
                server.sendmail(sender_email, sender.decode("utf-8"), message.encode("utf8"))
                server.close()
                print("Wiadomość została wysłana\n")
                imap.add_flags(msgid, '\Seen')
                imap.add_flags(msgid, '\Answered')
            else:
                print("Brak takiego adresu w bazie")
                messagezwrot = """Subject: Brak podanego adresu w bazie \n
                
                Dzień dobry,
                Odpowiadam na zgłoszenie z dnia {data}.\n
                Informuje, że adres e-mail {sender} nie znajduje się w bazie danych.\n
                Z wyrazami szacunku
                BOT ROD KONINKO """.format(sender=sender.decode("utf-8"), data=envelope.date)
                print("Rozpoczynam zwrot")
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.ehlo()  # Can be omitted
                server.login(sender_email, password_email)
                server.sendmail(sender_email, sender.decode("utf-8"), messagezwrot.encode("utf-8"))
                server.close()
                print("Wiadomość zwrotna została wysłana\n")
                imap.add_flags(msgid, '\Seen')
                imap.add_flags(msgid, '\Answered')
    print("Żadnych nowych maili spełniających kryteria. Zakończono pętlę!")
    for remaining in range(600, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} sekund do startu pętli.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rStart!            \n")