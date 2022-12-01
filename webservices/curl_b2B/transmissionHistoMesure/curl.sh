curl --verbose --user user:password \
    --key enedis-sge.com.key \
    --cert enedis-sge.com.fullchain.pem \
    -X POST -H "Content-Type: application/soap+xml" \
    --data-binary @f380r1.xml \
    https://sge-homologation-b2b.enedis.fr/CommandeTransmissionHistoriqueMesures/v1.0
date +"%T"