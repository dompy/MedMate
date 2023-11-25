import math
# Define test values for all parameters

# female qrisk3 calculation

def cvd_female_raw(age, b_AF, b_atypicalantipsy, b_corticosteroids, b_migraine, b_ra, b_renal, b_semi, b_sle, b_treatedhyp, b_type1, b_type2, bmi, ethrisk, fh_cvd, rati, sbp, sbps5, smoke_cat, surv, town):
    survivor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.988876402378082, 0, 0, 0, 0, 0]
    Iethrisk = [0, 0, 0.2804031433299542500000000, 0.5629899414207539800000000, 0.2959000085111651600000000, 0.0727853798779825450000000, -0.1707213550885731700000000, -0.3937104331487497100000000, -0.3263249528353027200000000, -0.1712705688324178400000000]
    Ismoke = [0, 0.1338683378654626200000000, 0.5620085801243853700000000, 0.6674959337750254700000000, 0.8494817764483084700000000]

    dage = age / 10
    age_1 = dage ** -2
    age_2 = dage

    dbmi = bmi / 10
    bmi_1 = dbmi ** -2
    bmi_2 = (dbmi ** -2) * math.log(dbmi)

    age_1 = age_1 - 0.053274843841791
    age_2 = age_2 - 4.332503318786621
    bmi_1 = bmi_1 - 0.154946178197861
    bmi_2 = bmi_2 - 0.144462317228317
    rati = rati - 3.476326465606690
    sbp = sbp - 123.130012512207030
    sbps5 = sbps5 - 9.002537727355957
    town = town - 0.392308831214905

    a = 0
    a += Iethrisk[ethrisk]
    a += Ismoke[smoke_cat]

    a += age_1 * -8.1388109247726188000000000
    a += age_2 * 0.7973337668969909800000000
    a += bmi_1 * 0.2923609227546005200000000
    a += bmi_2 * -4.1513300213837665000000000
    a += rati * 0.1533803582080255400000000
    a += sbp * 0.0131314884071034240000000
    a += sbps5 * 0.0078894541014586095000000
    a += town * 0.0772237905885901080000000

    a += b_AF * 1.5923354969269663000000000
    a += b_atypicalantipsy * 0.2523764207011555700000000
    a += b_corticosteroids * 0.5952072530460185100000000
    a += b_migraine * 0.3012672608703450000000000
    a += b_ra * 0.2136480343518194200000000
    a += b_renal * 0.6519456949384583300000000
    a += b_semi * 0.1255530805882017800000000
    a += b_sle * 0.7588093865426769300000000
    a += b_treatedhyp * 0.5093159368342300400000000
    a += b_type1 * 1.7267977510537347000000000
    a += b_type2 * 1.0688773244615468000000000
    a += fh_cvd * 0.4544531902089621300000000

    # Sum from interaction terms
    a += age_1 * (smoke_cat == 1) * -4.7057161785851891
    a += age_1 * (smoke_cat == 2) * -2.7430383403573337
    a += age_1 * (smoke_cat == 3) * -0.86608088829392182
    a += age_1 * (smoke_cat == 4) * 0.90241562369710648
    a += age_1 * b_AF * 19.938034889546561
    a += age_1 * b_corticosteroids * -0.98408045235936281
    a += age_1 * b_migraine * 1.7634979587872999
    a += age_1 * b_renal * -3.5874047731694114
    a += age_1 * b_sle * 19.690303738638292
    a += age_1 * b_treatedhyp * 11.872809733921812
    a += age_1 * b_type1 * -1.2444332714320747
    a += age_1 * b_type2 * 6.8652342000009599
    a += age_1 * bmi_1 * 23.802623412141742
    a += age_1 * bmi_2 * -71.184947692087007
    a += age_1 * fh_cvd * 0.99467807940435127
    a += age_1 * sbp * 0.034131842338615485
    a += age_1 * town * -1.0301180802035639
    a += age_2 * (smoke_cat == 1) * -0.075589244643193026
    a += age_2 * (smoke_cat == 2) * -0.11951192874867074
    a += age_2 * (smoke_cat == 3) * -0.10366306397571923
    a += age_2 * (smoke_cat == 4) * -0.13991853591718389
    a += age_2 * b_AF * -0.076182651011162505
    a += age_2 * b_corticosteroids * -0.12005364946742472
    a += age_2 * b_migraine * -0.065586917898699859
    a += age_2 * b_renal * -0.22688873086442507
    a += age_2 * b_sle * 0.077347949679016273
    a += age_2 * b_treatedhyp * 0.00096857823588174436
    a += age_2 * b_type1 * -0.28724064624488949
    a += age_2 * b_type2 * -0.097112252590695489
    a += age_2 * bmi_1 * 0.52369958933664429
    a += age_2 * bmi_2 * 0.045744190122323759
    a += age_2 * fh_cvd * -0.076885051698423038
    a += age_2 * sbp * -0.0015082501423272358
    a += age_2 * town * -0.031593414674962329

    # Calculate the score itself
    scorew = 100.0 * (1 - (survivor[surv] ** math.exp(a)))
    return scorew

if __name__ == "__main__":
    score = cvd_female_raw(age, b_AF, b_atypicalantipsy, b_corticosteroids, b_migraine, b_ra, b_renal, b_semi, b_sle, b_treatedhyp, b_type1, b_type2, bmi, ethrisk, fh_cvd, rati, sbp, sbps5, smoke_cat, surv, town)