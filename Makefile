DATE=`date +%Y-%m-%d`
TRAITER='./traiter'
TRAITS= -t life_stage -t sex -t testes_state -t testes_size -t total_length
TRAITS+= -t tail_length -t hind_foot_length -t ear_length -t body_mass
ASIS= -a sex:sex -a lifestage:life_stage
SEARCH= -s dynamicproperties -s occurrenceremarks -s fieldnotes
SEARCH+= -s reproductivecondition
EXTRA= -e occurrenceid -e scientificname -e eventdate -e collectioncode
EXTRA+= -e institutioncode -e catalognumber -e recordedby
EXTRA+= -e decimallatitude -e decimallongitude -e locality -e references
EXTRA+= -e minimumelevationinmeters -e maximumelevationinmeters
ARGS= --log-every 1000
RAW=data/raw
OUTPUT=output
TARGETS=sciurus tamias urocitellus

all: $(TARGETS)

$(TARGETS): $(RAW)/$@.csv
	time $(TRAITER) $TRAITS $ASIS $SEARCH $EXTRA $ARGS $< $(OUTPUT)/$@_$(DATE).csv
	time $(TRAITER) $TRAITS $ASIS $SEARCH $EXTRA $ARGS $< $(OUTPUT)/$@_$(DATE).html -o html
