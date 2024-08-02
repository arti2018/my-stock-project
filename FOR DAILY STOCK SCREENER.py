import yfinance as yf
import pandas as pd
from datetime import datetime

def calculate_fibonacci_pivots(high, low, close):
    pivot = (high + low + close) / 3
    range_ = high - low
    s1 = pivot - (range_ * 0.382)
    s2 = pivot - (range_ * 0.618)
    s3 = pivot - (range_ * 1.000)
    r1 = pivot + (range_ * 0.382)
    r2 = pivot + (range_ * 0.618)
    r3 = pivot + (range_ * 1.000)
    return s1, s2, s3, r1, r2, r3

def check_stocks_touching_s3(stock_list, year):
    previous_year = year - 1
    start_date = datetime(previous_year, 1, 1)
    end_date = datetime(year, 1, 1)

    stocks_touching_s3 = []
    stocks_with_no_data = []

    for stock in stock_list:
        try:
            # Fetch historical data for the previous year
            data = yf.download(stock, start=start_date, end=end_date, progress=False)

            if data.empty:
                stocks_with_no_data.append(stock)
                continue

            yearly_high = data['High'].max()
            yearly_low = data['Low'].min()
            yearly_close = data['Close'][-1]

            # Calculate S3 level using previous year's data
            s1, s2, s3, r1, r2, r3 = calculate_fibonacci_pivots(yearly_high, yearly_low, yearly_close)

            # Fetch data for the current year to check if S3 level was touched
            current_year_start_date = datetime(year, 1, 1)
            current_year_end_date = datetime(year + 1, 1, 1)
            latest_data = yf.download(stock, start=current_year_start_date, end=current_year_end_date, progress=False)

            if latest_data.empty:
                stocks_with_no_data.append(stock)
                continue

            # Check if the stock touches S3 level in the current year
            touched_s3 = latest_data['Low'].min() <= s3

            if touched_s3:
                stocks_touching_s3.append(stock)

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            stocks_with_no_data.append(stock)

    return stocks_touching_s3, stocks_with_no_data

def get_in_stock_list():
    indian_stocks = [
        "3MINDIA.NS",
"AARTIIND.NS",
"AAVAS.NS",
"ABB.NS",
"ABCAPITAL.NS",
"ABFRL.NS",
"ABSLAMC.NS",
"ACC.NS",
"ACE.NS",
"ACI.NS",
"ADANIENT.NS",
"ADANIGREEN.NS",
"ADANIPORTS.NS",
"ADANIPOWER.NS",
"AEGISCHEM.NS",
"AETHER.NS",
"AFFLE.NS",
"AHLUCONT.NS",
"AIAENG.NS",
"AJANTPHARM.NS",
"AKZOINDIA.NS",
"ALKEM.NS",
"ALKYLAMINE.NS",
"ALLCARGO.NS",
"ALOKINDS.NS",
"AMBER.NS",
"AMBUJACEM.NS",
"ANANDRATHI.NS",
"ANANTRAJ.NS",
"ANGELONE.NS",
"ANURAS.NS",
"APARINDS.NS",
"APLAPOLLO.NS",
"APLLTD.NS",
"APOLLOHOSP.NS",
"APOLLOTYRE.NS",
"APTUS.NS",
"ARE&M.NS",
"ARVIND.NS",
"ARVINDFASN.NS",
"ASAHIINDIA.NS",
"ASHOKLEY.NS",
"ASIANPAINT.NS",
"ASTERDM.NS",
"ASTRAL.NS",
"ASTRAMICRO.NS",
"ASTRAZEN.NS",
"ATGL.NS",
"ATUL.NS",
"AUBANK.NS",
"AURIONPRO.NS",
"AUROPHARMA.NS",
"AVANTIFEED.NS",
"AWL.NS",
"AXISBANK.NS",
"AZAD.NS",
"BAJAJ-AUTO.NS",
"BAJAJELEC.NS",
"BAJAJFINSV.NS",
"BAJAJHLDNG.NS",
"BAJFINANCE.NS",
"BALAMINES.NS",
"BALKRISIND.NS",
"BALRAMCHIN.NS",
"BANDHANBNK.NS",
"BANKBARODA.NS",
"BANKINDIA.NS",
"BASF.NS",
"BATAINDIA.NS",
"BBTC.NS",
"BDL.NS",
"BECTORFOOD.NS",
"BEL.NS",
"BEML.NS",
"BERGEPAINT.NS",
"BHARATFORG.NS",
"BHARTIARTL.NS",
"BHEL.NS",
"BIKAJI.NS",
"BIOCON.NS",
"BIRLACORPN.NS",
"BLS.NS",
"BLUEDART.NS",
"BLUEJET.NS",
"BLUESTARCO.NS",
"BORORENEW.NS",
"BOSCHLTD.NS",
"BPCL.NS",
"BRIGADE.NS",
"BRITANNIA.NS",
"BSE.NS",
"BSOFT.NS",
"CAMPUS.NS",
"CAMS.NS",
"CANBK.NS",
"CANFINHOME.NS",
"CAPLIPOINT.NS",
"CARBORUNIV.NS",
"CASTROLIND.NS",
"CCL.NS",
"CDSL.NS",
"CEATLTD.NS",
"CELLO.NS",
"CENTRALBK.NS",
"CENTURYPLY.NS",
"CENTURYTEX.NS",
"CERA.NS",
"CESC.NS",
"CGPOWER.NS",
"CHALET.NS",
"CHAMBLFERT.NS",
"CHEMPLASTS.NS",
"CHENNPETRO.NS",
"CHOICEIN.NS",
"CHOLAFIN.NS",
"CHOLAHLDNG.NS",
"CIEINDIA.NS",
"CIPLA.NS",
"CLEAN.NS",
"CMSINFO.NS",
"COALINDIA.NS",
"COCHINSHIP.NS",
"COFORGE.NS",
"COLPAL.NS",
"CONCOR.NS",
"CONCORDBIO.NS",
"COROMANDEL.NS",
"CRAFTSMAN.NS",
"CREDITACC.NS",
"CRISIL.NS",
"CROMPTON.NS",
"CSBBANK.NS",
"CUB.NS",
"CUMMINSIND.NS",
"CYIENT.NS",
"CYIENTDLM.NS",
"DABUR.NS",
"DALBHARAT.NS",
"DATAPATTNS.NS",
"DBL.NS",
"DBREALTY.NS",
"DCMSHRIRAM.NS",
"DEEPAKFERT.NS",
"DEEPAKNTR.NS",
"DELHIVERY.NS",
"DEVYANI.NS",
"DIVISLAB.NS",
"DIXON.NS",
"DLF.NS",
"DMART.NS",
"DRREDDY.NS",
"EASEMYTRIP.NS",
"ECLERX.NS",
"EDELWEISS.NS",
"EICHERMOT.NS",
"EIDPARRY.NS",
"EIHOTEL.NS",
"ELECON.NS",
"ELECTCAST.NS",
"ELGIEQUIP.NS",
"EMAMILTD.NS",
"EMIL.NS",
"EMUDHRA.NS",
"ENDURANCE.NS",
"ENGINERSIN.NS",
"EPL.NS",
"EQUITASBNK.NS",
"ERIS.NS",
"ESABINDIA.NS",
"ESCORTS.NS",
"ETHOSLTD.NS",
"EXIDEIND.NS",
"FACT.NS",
"FDC.NS",
"FEDERALBNK.NS",
"FINCABLES.NS",
"FINEORG.NS",
"FINPIPE.NS",
"FIVESTAR.NS",
"FLUOROCHEM.NS",
"FORCEMOT.NS",
"FORTIS.NS",
"FSL.NS",
"GAEL.NS",
"GAIL.NS",
"GALAXYSURF.NS",
"GANESHHOUC.NS",
"GARFIBRES.NS",
"GENUSPOWER.NS",
"GESHIP.NS",
"GET&D.NS",
"GICRE.NS",
"GILLETTE.NS",
"GLAND.NS",
"GLAXO.NS",
"GLENMARK.NS",
"GLS.NS",
"GMDCLTD.NS",
"GMMPFAUDLR.NS",
"GMRINFRA.NS",
"GNFC.NS",
"GOCOLORS.NS",
"GODFRYPHLP.NS",
"GODREJAGRO.NS",
"GODREJCP.NS",
"GODREJIND.NS",
"GODREJPROP.NS",
"GPIL.NS",
"GPPL.NS",
"GRANULES.NS",
"GRAPHITE.NS",
"GRASIM.NS",
"GRAVITA.NS",
"GREENLAM.NS",
"GRINDWELL.NS",
"GRINFRA.NS",
"GRSE.NS",
"GSFC.NS",
"GSPL.NS",
"GUJGASLTD.NS",
"HAL.NS",
"HATSUN.NS",
"HAVELLS.NS",
"HBLPOWER.NS",
"HCC.NS",
"HCLTECH.NS",
"HDFCAMC.NS",
"HDFCBANK.NS",
"HDFCLIFE.NS",
"HEG.NS",
"HEMIPROP.NS",
"HEROMOTOCO.NS",
"HFCL.NS",
"HGINFRA.NS",
"HINDALCO.NS",
"HINDCOPPER.NS",
"HINDPETRO.NS",
"HINDUNILVR.NS",
"HINDZINC.NS",
"HNDFDS.NS",
"HOMEFIRST.NS",
"HONAUT.NS",
"HSCL.NS",
"HUDCO.NS",
"IBREALEST.NS",
"IBULHSGFIN.NS",
"ICICIBANK.NS",
"ICICIGI.NS",
"ICICIPRULI.NS",
"ICIL.NS",
"IDBI.NS",
"IDEA.NS",
"IDFC.NS",
"IDFCFIRSTB.NS",
"IEX.NS",
"IFBIND.NS",
"IFCI.NS",
"IGL.NS",
"IIFL.NS",
"INDHOTEL.NS",
"INDIACEM.NS",
"INDIAMART.NS",
"INDIANB.NS",
"INDIASHLTR.NS",
"INDIGO.NS",
"INDIGOPNTS.NS",
"INDUSINDBK.NS",
"INDUSTOWER.NS",
"INFIBEAM.NS",
"INFY.NS",
"INGERRAND.NS",
"INOXINDIA.NS",
"INOXWIND.NS",
"INTELLECT.NS",
"IOB.NS",
"IOC.NS",
"IONEXCHANG.NS",
"IPCALAB.NS",
"IRB.NS",
"IRCON.NS",
"IRCTC.NS",
"IREDA.NS",
"IRFC.NS",
"ISEC.NS",
"ISGEC.NS",
"ITC.NS",
"ITDC.NS",
"ITDCEM.NS",
"ITI.NS",
"IWEL.NS",
"J&KBANK.NS",
"JAIBALAJI.NS",
"JAMNAAUTO.NS",
"JBCHEPHARM.NS",
"JBMA.NS",
"JINDALSAW.NS",
"JINDALSTEL.NS",
"JINDWORLD.NS",
"JKCEMENT.NS",
"JKLAKSHMI.NS",
"JKPAPER.NS",
"JKTYRE.NS",
"JLHL.NS",
"JMFINANCIL.NS",
"JPPOWER.NS",
"JSL.NS",
"JSWENERGY.NS",
"JSWHL.NS",
"JSWINFRA.NS",
"JSWSTEEL.NS",
"JUBLFOOD.NS",
"JUBLINGREA.NS",
"JUBLPHARMA.NS",
"JUSTDIAL.NS",
"JWL.NS",
"JYOTHYLAB.NS",
"KAJARIACER.NS",
"KALYANKJIL.NS",
"KANSAINER.NS",
"KARURVYSYA.NS",
"KAYNES.NS",
"KEC.NS",
"KEI.NS",
"KESORAMIND.NS",
"KFINTECH.NS",
"KIMS.NS",
"KIOCL.NS",
"KIRLOSBROS.NS",
"KIRLOSENG.NS",
"KNRCON.NS",
"KOTAKBANK.NS",
"KPIGREEN.NS",
"KPIL.NS",
"KPITTECH.NS",
"KPRMILL.NS",
"KRBL.NS",
"KSB.NS",
"KTKBANK.NS",
"LALPATHLAB.NS",
"LATENTVIEW.NS",
"LAURUSLABS.NS",
"LAXMIMACH.NS",
"LEMONTREE.NS",
"LICHSGFIN.NS",
"LICI.NS",
"LINDEINDIA.NS",
"LLOYDSME.NS",
"LODHA.NS",
"LT.NS",
"LTIM.NS",
"LTTS.NS",
"LUPIN.NS",
"LXCHEM.NS",
"M&M.NS",
"M&MFIN.NS",
"MAHABANK.NS",
"MAHLIFE.NS",
"MAHSCOOTER.NS",
"MAHSEAMLES.NS",
"MANAPPURAM.NS",
"MANINFRA.NS",
"MANYAVAR.NS",
"MAPMYINDIA.NS",
"MARICO.NS",
"MARKSANS.NS",
"MARUTI.NS",
"MASTEK.NS",
"MAXHEALTH.NS",
"MAZDOCK.NS",
"MCDOWELL-N.NS",
"MEDANTA.NS",
"MEDPLUS.NS",
"METROBRAND.NS",
"METROPOLIS.NS",
"MFSL.NS",
"MGL.NS",
"MHRIL.NS",
"MIDHANI.NS",
"MINDACORP.NS",
"MMTC.NS",
"MOIL.NS",
"MOTHERSON.NS",
"MOTILALOFS.NS",
"MPHASIS.NS",
"MRF.NS",
"MRPL.NS",
"MSTCLTD.NS",
"MSUMI.NS",
"MUTHOOTFIN.NS",
"NAM-INDIA.NS",
"NATCOPHARM.NS",
"NATIONALUM.NS",
"NAUKRI.NS",
"NAVA.NS",
"NAVINFLUOR.NS",
"NBCC.NS",
"NCC.NS",
"NESCO.NS",
"NESTLEIND.NS",
"NETWEB.NS",
"NETWORK18.NS",
"NEULANDLAB.NS",
"NEWGEN.NS",
"NH.NS",
"NHPC.NS",
"NIACL.NS",
"NIITMTS.NS",
"NLCINDIA.NS",
"NMDC.NS",
"NTPC.NS",
"NUVOCO.NS",
"NYKAA.NS",
"OBEROIRLTY.NS",
"OFSS.NS",
"OIL.NS",
"OLECTRA.NS",
"ONGC.NS",
"ORCHPHARMA.NS",
"PAGEIND.NS",
"PAISALO.NS",
"PARADEEP.NS",
"PATANJALI.NS",
"PAYTM.NS",
"PCBL.NS",
"PDSL.NS",
"PEL.NS",
"PERSISTENT.NS",
"PETRONET.NS",
"PFC.NS",
"PFIZER.NS",
"PGHH.NS",
"PGHL.NS",
"PHOENIXLTD.NS",
"PIDILITIND.NS",
"PIIND.NS",
"PNB.NS",
"PNBHOUSING.NS",
"PNCINFRA.NS",
"POLICYBZR.NS",
"POLYCAB.NS",
"POLYMED.NS",
"POONAWALLA.NS",
"POWERGRID.NS",
"POWERINDIA.NS",
"POWERMECH.NS",
"PPLPHARMA.NS",
"PRAJIND.NS",
"PRESTIGE.NS",
"PRINCEPIPE.NS",
"PRSMJOHNSN.NS",
"PSB.NS",
"PTC.NS",
"PVRINOX.NS",
"QUESS.NS",
"RADICO.NS",
"RAILTEL.NS",
"RAINBOW.NS",
"RAJESHEXPO.NS",
"RAMCOCEM.NS",
"RATEGAIN.NS",
"RATNAMANI.NS",
"RAYMOND.NS",
"RBLBANK.NS",
"RCF.NS",
"RECLTD.NS",
"RELIANCE.NS",
"REDINGTON.NS",
"RELAXO.NS",
"RELIGARE.NS",
"RELINFRA.NS",
"RENUKA.NS",
"RESPONIND.NS",
"RHIM.NS",
"RITES.NS",
"RKFORGE.NS",
"ROUTE.NS",
"RPOWER.NS",
"RRKABEL.NS",
"RTNINDIA.NS",
"RUSTOMJEE.NS",
"RVNL.NS",
"SAFARI.NS",
"SAIL.NS",
"SANGHVIMOV.NS",
"SANOFI.NS",
"SANSERA.NS",
"SAPPHIRE.NS",
"SARDAEN.NS",
"SAREGAMA.NS",
"SBFC.NS",
"SBICARD.NS",
"SBILIFE.NS",
"SBIN.NS",
"SCHAEFFLER.NS",
"SCHNEIDER.NS",
"SCI.NS",
"SFL.NS",
"SHAREINDIA.NS",
"SHOPERSTOP.NS",
"SHREECEM.NS",
"SHRIPISTON.NS",
"SHRIRAMFIN.NS",
"SHYAMMETL.NS",
"SIEMENS.NS",
"SIS.NS",
"SJVN.NS",
"SKFINDIA.NS",
"SOBHA.NS",
"SOLARINDS.NS",
"SONACOMS.NS",
"SONATSOFTW.NS",
"SOUTHBANK.NS",
"SPANDANA.NS",
"SPARC.NS",
"SPLPETRO.NS",
"SRF.NS",
"STAR.NS",
"STARCEMENT.NS",
"STARHEALTH.NS",
"SUMICHEM.NS",
"SUNDARMFIN.NS",
"SUNDRMFAST.NS",
"SUNPHARMA.NS",
"SUNTECK.NS",
"SUNTV.NS",
"SUPRAJIT.NS",
"SUPREMEIND.NS",
"SURYAROSNI.NS",
"SUVENPHAR.NS",
"SUZLON.NS",
"SWANENERGY.NS",
"SWSOLAR.NS",
"SYMPHONY.NS",
"SYNGENE.NS",
"SYRMA.NS",
"TANLA.NS",
"TATACHEM.NS",
"TATACOMM.NS",
"TATACONSUM.NS",
"TATAELXSI.NS",
"TATAINVEST.NS",
"TATAMOTORS.NS",
"TATAPOWER.NS",
"TATASTEEL.NS",
"TCI.NS",
"TCS.NS",
"TECHM.NS",
"TECHNOE.NS",
"TEGA.NS",
"TEJASNET.NS",
"TEXRAIL.NS",
"THERMAX.NS",
"THOMASCOOK.NS",
"TIINDIA.NS",
"TIMETECHNO.NS",
"TIMKEN.NS",
"TIPSINDLTD.NS",
"TITAGARH.NS",
"TITAN.NS",
"TMB.NS",
"TORNTPHARM.NS",
"TORNTPOWER.NS",
"TRENT.NS",
"TRIDENT.NS",
"TRIL.NS",
"TRITURBINE.NS",
"TRIVENI.NS",
"TTKPRESTIG.NS",
"TTML.NS",
"TV18BRDCST.NS",
"TVSHLTD.NS",
"TVSMOTOR.NS",
"UBL.NS",
"UCOBANK.NS",
"UJJIVANSFB.NS",
"ULTRACEMCO.NS",
"UNIONBANK.NS",
"UNOMINDA.NS",
"UPL.NS",
"USHAMART.NS",
"UTIAMC.NS",
"VAIBHAVGBL.NS",
"VARROC.NS",
"VBL.NS",
"VEDL.NS",
"VESUVIUS.NS",
"VGUARD.NS",
"VIJAYA.NS",
"VINATIORGA.NS",
"VIPIND.NS",
"VOLTAMP.NS",
"VOLTAS.NS",
"VSTIND.NS",
"VTL.NS",
"WELCORP.NS",
"WELSPUNLIV.NS",
"WESTLIFE.NS",
"WHIRLPOOL.NS",
"WIPRO.NS",
"WOCKPHARMA.NS",
"WONDERLA.NS",
"YESBANK.NS",
"ZEEL.NS",
"ZENSARTECH.NS",
"ZENTEC.NS",
"ZFCVINDIA.NS",
"ZOMATO.NS",
"ZYDUSLIFE.NS",
"ZYDUSWELL.NS"

    ]
    return indian_stocks

# Fetch the list of Indian stocks
indian_stocks = get_in_stock_list()

# Set the desired year to check which stocks touched the S3 level
desired_year = 2024

# Get stocks that touched S3 and those with no data for the specified year
stocks_touching_s3, stocks_with_no_data = check_stocks_touching_s3(indian_stocks, desired_year)

# Output results
print(f"Stocks that touched S3 in {desired_year}: {stocks_touching_s3}")
print(f"Stocks with no data in {desired_year}: {stocks_with_no_data}")
