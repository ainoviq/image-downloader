from asyncio.log import logger
from logging import warning
import time
import scrapy


class FleeceSpider(scrapy.Spider):
    name = 'marcus'

    def __init__(self, *args, **kwargs):
        super(FleeceSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        link_elements = [
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-pique-flag-trim-polo-shirt-prod245240054?childItemId=NMN89V5_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=0",
            "https://www.neimanmarcus.com/en-bd/p/brunello-cucinelli-mens-jersey-polo-shirt-prod251530250?childItemId=NMN97YF_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=1",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-tb-polo-shirt-prod252400087?childItemId=NMN9K8Y_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=2",
            "https://www.neimanmarcus.com/en-bd/p/rag-bone-mens-interlock-cotton-polo-shirt-prod252890132?childItemId=NMN9N6Q_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=3",
            "https://www.neimanmarcus.com/en-bd/p/onia-mens-linen-polo-shirt-prod249660377?childItemId=NMN91WA_41&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=4",
            "https://www.neimanmarcus.com/en-bd/p/brioni-mens-cotton-silk-polo-shirt-prod253110190?childItemId=NMN9NR7_20&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=5",
            "https://www.neimanmarcus.com/en-bd/p/versace-jeans-couture-mens-logo-polo-shirt-prod252510069?childItemId=NMN9L0V_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=6",
            "https://www.neimanmarcus.com/en-bd/p/tom-ford-mens-garment-dyed-piquet-polo-shirt-prod253710098?childItemId=NMN9JXB_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=7",
            "https://www.neimanmarcus.com/en-bd/p/dolce-gabbana-mens-dg-tipped-polo-shirt-prod252800008?childItemId=NMN9MAK_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=8",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-logo-tape-harness-polo-shirt-prod236820085?childItemId=NMN7PJQ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=9",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-tb-logo-polo-shirt-prod252400461?childItemId=NMN9K9S_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=10",
            "https://www.neimanmarcus.com/en-bd/p/derek-rose-mens-paris-22-modern-long-pajama-set-prod248310131?childItemId=NMN8WL0_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=11",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-tb-polo-shirt-prod252400095?childItemId=NMN9K7V_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=12",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-harness-polo-shirt-prod243740250?childItemId=NMN8DND_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=13",
            "https://www.neimanmarcus.com/en-bd/p/boss-mens-two-tone-zip-polo-shirt-prod254950027?childItemId=NMN9HHF_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=14",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-classic-tipped-polo-shirt-prod252850298?childItemId=NMN9MUM_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=15",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-contrast-collar-polo-shirt-prod247580327?childItemId=NMN8T31_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=16",
            "https://www.neimanmarcus.com/en-bd/p/lacoste-mens-signature-polo-shirt-prod248850083?childItemId=NMN8YZ8_30&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=17",
            "https://www.neimanmarcus.com/en-bd/p/emporio-armani-mens-geometric-print-stretch-polo-shirt-prod252210119?childItemId=NMN9ATW_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=18",
            "https://www.neimanmarcus.com/en-bd/p/boss-mens-polo-shirt-w-trim-details-prod255020267?childItemId=NMN9HH7_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=19",
            "https://www.neimanmarcus.com/en-bd/p/rodd-gunn-mens-new-haven-heathered-polo-shirt-prod226880253?childItemId=NMN6R5B_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=20",
            "https://www.neimanmarcus.com/en-bd/p/rodd-gunn-mens-the-gunn-polo-shirt-prod229950281?childItemId=NMN70LP_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=21",
            "https://www.neimanmarcus.com/en-bd/p/bugatchi-mens-1-4-zip-tipped-polo-shirt-prod249960187?childItemId=NMN93W2_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=22",
            "https://www.neimanmarcus.com/en-bd/p/theory-mens-bron-c-cosmos-polo-shirt-prod238610198?childItemId=NMN7Z0V_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=23",
            "https://www.neimanmarcus.com/en-bd/p/maceoo-mens-mozart-contrast-trim-polo-shirt-prod254080153?childItemId=NMN9TK3_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=24",
            "https://www.neimanmarcus.com/en-bd/p/versace-jeans-couture-mens-flocked-logo-polo-shirt-prod252510067?childItemId=NMN9L1N_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=25",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-tipped-polo-shirt-prod247580133?childItemId=NMN8T3A_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=26",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-edney-polo-shirt-w-logo-collar-prod240040081?childItemId=NMN83UN_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=27",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-sean-stretch-jersey-polo-shirt-prod241122122?childItemId=NMN61VQ_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=28",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-tb-logo-polo-shirt-prod252400397?childItemId=NMN9K8J_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=29",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-oversized-graffiti-print-pique-polo-shirt-prod252400415?childItemId=NMN9AVV_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=30",
            "https://www.neimanmarcus.com/en-bd/p/onia-mens-linen-polo-shirt-prod254710169?childItemId=NMN9NC8_41&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=31",
            "https://www.neimanmarcus.com/en-bd/p/brunello-cucinelli-mens-solid-pique-polo-shirt-prod220400153?childItemId=NMN65MY_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=32",
            "https://www.neimanmarcus.com/en-bd/p/emporio-armani-mens-geometric-print-stretch-polo-shirt-prod252210090?childItemId=NMN9ATV_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=33",
            "https://www.neimanmarcus.com/en-bd/p/dolce-gabbana-mens-dg-collar-polo-shirt-prod253110016?childItemId=NMN9NYS_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=34",
            "https://www.neimanmarcus.com/en-bd/p/ralph-lauren-purple-label-mens-striped-polo-shirt-prod246960391?childItemId=NMN8QJH_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=35",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-pique-logo-tape-polo-shirt-prod252420043?childItemId=NMN9AVY_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=36",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-polo-shirt-w-logo-taping-prod253140121?childItemId=NMN9NV8_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=37",
            "https://www.neimanmarcus.com/en-bd/p/salvatore-ferragamo-mens-gancini-collar-polo-shirt-prod249610007?childItemId=NMN92CR_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=38",
            "https://www.neimanmarcus.com/en-bd/p/maceoo-mens-mozart-luxe-colorblock-polo-shirt-prod254070054?childItemId=NMN9TJT_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=39",
            "https://www.neimanmarcus.com/en-bd/p/fisher-baker-mens-watson-solid-polo-shirt-prod231550391?childItemId=NMN74J1_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=40",
            "https://www.neimanmarcus.com/en-bd/p/kiton-mens-cotton-cashmere-polo-shirt-prod252510104?childItemId=NMN9KWY_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=41",
            "https://www.neimanmarcus.com/en-bd/p/salvatore-ferragamo-mens-gancini-polo-shirt-prod245560285?childItemId=NMN8LU3_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=42",
            "https://www.neimanmarcus.com/en-bd/p/givenchy-mens-classic-fit-logo-zip-polo-shirt-prod252200035?childItemId=NMN9J9J_9Q&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=43",
            "https://www.neimanmarcus.com/en-bd/p/boss-mens-polo-shirt-with-striped-trim-prod253050122?childItemId=NMN9HHT_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=44",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-oversized-graffiti-collar-polo-shirt-prod252400291?childItemId=NMN9KCV_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=45",
            "https://www.neimanmarcus.com/en-bd/p/eton-mens-contemporary-fit-short-sleeve-polo-prod248530253?childItemId=NMN8XH0_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=46",
            "https://www.neimanmarcus.com/en-bd/p/rodd-gunn-mens-stanley-point-jacquard-polo-shirt-prod253270169?childItemId=NMN9Q1W_2L&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=47",
            "https://www.neimanmarcus.com/en-bd/p/maceoo-mens-mozart-solid-floral-trim-polo-shirt-prod254070103?childItemId=NMN9TK4_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=48",
            "https://www.neimanmarcus.com/en-bd/p/vilebrequin-mens-terry-knit-polo-shirt-prod211740396?childItemId=NMN5GKJ_41&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=49",
            "https://www.neimanmarcus.com/en-bd/p/kiton-mens-cotton-cashmere-polo-shirt-prod250130059?childItemId=NMN94PC_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=50",
            "https://www.neimanmarcus.com/en-bd/p/dolce-gabbana-mens-dg-graffiti-polo-shirt-prod253110014?childItemId=NMN9NYR_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=51",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-wellman-check-knit-polo-shirt-prod252400268?childItemId=NMN9K85_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=52",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-tb-polo-shirt-prod252400412?childItemId=NMN9K9U_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=53",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-embroidered-logo-polo-shirt-prod247360100?childItemId=NMN8S5P_42&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=54",
            "https://www.neimanmarcus.com/en-bd/p/versace-jeans-couture-mens-tapestry-polo-shirt-prod252510053?childItemId=NMN9L0G_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=55",
            "https://www.neimanmarcus.com/en-bd/p/versace-jeans-couture-mens-baroque-logo-polo-shirt-prod252510495?childItemId=NMN9L4B_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=56",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-pierson-icon-stripe-polo-shirt-prod252400368?childItemId=NMN9K78_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=57",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-eddie-pique-polo-shirt-gray-prod222154214?childItemId=NMN69UM_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=58",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-pierson-icon-stripe-polo-shirt-prod252400430?childItemId=NMN9K8V_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=59",
            "https://www.neimanmarcus.com/en-bd/p/ralph-lauren-purple-label-mens-embroidered-bear-polo-shirt-prod246950011?childItemId=NMN8QJQ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=60",
            "https://www.neimanmarcus.com/en-bd/p/versace-mens-greca-collar-polo-shirt-prod251550029?childItemId=NMN99QG_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=61",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-pierson-check-trim-polo-shirt-prod252400132?childItemId=NMN9K94_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=62",
            "https://www.neimanmarcus.com/en-bd/p/salvatore-ferragamo-mens-piped-zip-logo-polo-shirt-prod249610008?childItemId=NMN92CS_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=63",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-snap-polo-shirt-prod247580096?childItemId=NMN8T3U_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=64",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-perrywood-logo-patch-polo-shirt-prod252100302?childItemId=NMN9BGZ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=65",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-perrywood-tb-pique-polo-shirt-prod252080440?childItemId=NMN9BGT_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=66",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-logo-collar-polo-shirt-prod252850399?childItemId=NMN9MU9_41&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=67",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-drum-performance-jersey-polo-shirt-prod252710108?childItemId=NMN9L9V_41&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=68",
            "https://www.neimanmarcus.com/en-bd/p/vince-classic-slub-cotton-polo-shirt-prod228410267?childItemId=NMN6VRC_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=69",
            "https://www.neimanmarcus.com/en-bd/p/ralph-lauren-mens-bear-patch-polo-shirt-prod246960409?childItemId=NMN8QJM_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=70",
            "https://www.neimanmarcus.com/en-bd/p/theory-mens-bron-classic-polo-shirt-prod251970089?childItemId=NMN9ARH_20&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=71",
            "https://www.neimanmarcus.com/en-bd/p/givenchy-mens-peace-logo-zip-polo-shirt-prod252190060?childItemId=NMN9J9V_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=72",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-signature-polo-shirt-prod242800168?childItemId=NMN8AXY_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=73",
            "https://www.neimanmarcus.com/en-bd/p/zegna-mens-cotton-stretch-polo-shirt-prod247610051?childItemId=NMN8TD8_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=74",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-logo-tape-polo-shirt-prod252850384?childItemId=NMN9MU1_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=75",
            "https://www.neimanmarcus.com/en-bd/p/alexander-mcqueen-mens-logo-polo-shirt-prod238600130?childItemId=NMN7YXR_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=76",
            "https://www.neimanmarcus.com/en-bd/p/tom-ford-mens-garment-dyed-piquet-polo-shirt-prod253720008?childItemId=NMN9JXP_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=77",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-edit-solid-logo-polo-shirt-prod247570052?childItemId=NMN8T39_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=78",
            "https://www.neimanmarcus.com/en-bd/p/tom-ford-mens-garment-dyed-piquet-polo-shirt-prod253710135?childItemId=NMN9JXD_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=79",
            "https://www.neimanmarcus.com/en-bd/p/tom-ford-mens-garment-dyed-piquet-polo-shirt-prod253650256?childItemId=NMN9JX2_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=80",
            "https://www.neimanmarcus.com/en-bd/p/emporio-armani-basic-textured-polo-shirt-prod206150002?childItemId=NMN55L8_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=81",
            "https://www.neimanmarcus.com/en-bd/p/boss-mens-polo-shirt-with-striped-trim-prod253040057?childItemId=NMN9HHC_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=82",
            "https://www.neimanmarcus.com/en-bd/p/lacoste-mens-organic-stretch-cotton-pique-polo-shirt-prod249450101?childItemId=NMN91XZ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=83",
            "https://www.neimanmarcus.com/en-bd/p/lacoste-mens-monogram-print-polo-shirt-prod249450291?childItemId=NMN91XQ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=84",
            "https://www.neimanmarcus.com/en-bd/p/burberry-mens-hadleigh-check-logo-zip-polo-shirt-prod250360116?childItemId=NMN95R1_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=85",
            "https://www.neimanmarcus.com/en-bd/p/theory-mens-tipped-pique-polo-shirt-prod252720172?childItemId=NMN9LZB_MN&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=86",
            "https://www.neimanmarcus.com/en-bd/p/bugatchi-mens-striped-mercerized-cotton-polo-shirt-with-contrast-collar-cuffs-prod250920375?childItemId=NMN97Q0_4P&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=87",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-jubilee-stripe-stretch-jersey-polo-shirt-prod212080310?childItemId=NMN5H7G_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=88",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-tipped-cotton-pique-polo-shirt-prod240670177?childItemId=NMN85VB_H7&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=89",
            "https://www.neimanmarcus.com/en-bd/p/ralph-lauren-purple-label-mens-jersey-pocket-polo-shirt-navy-prod222151508?childItemId=NMN69QZ_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=90",
            "https://www.neimanmarcus.com/en-bd/p/versace-jeans-couture-mens-metallic-logo-polo-shirt-prod249220144?childItemId=NMN8WZ0_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=91",
            "https://www.neimanmarcus.com/en-bd/p/zegna-mens-cotton-stretch-polo-shirt-prod247610030?childItemId=NMN8TDV_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=92",
            "https://www.neimanmarcus.com/en-bd/p/salvatore-ferragamo-mens-gancini-polo-shirt-prod249590094?childItemId=NMN92CL_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=93",
            "https://www.neimanmarcus.com/en-bd/p/boss-mens-polo-shirt-with-trim-details-prod254840092?childItemId=NMN9HHS_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=94",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-stretch-jersey-polo-shirt-prod212010182?childItemId=NMN5H7E_42&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=95",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-lava-wash-cotton-stretch-henley-t-shirt-prod252710080?childItemId=NMN9L9G_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=96",
            "https://www.neimanmarcus.com/en-bd/p/rag-bone-mens-interlock-knit-polo-shirt-prod254560116?childItemId=NMN9VEC_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=97",
            "https://www.neimanmarcus.com/en-bd/p/balmain-mens-mega-monogram-houndstooth-knit-polo-shirt-prod251490190?childItemId=NMN99EF_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=98",
            "https://www.neimanmarcus.com/en-bd/p/dolce-gabbana-mens-crest-tipped-polo-shirt-prod252810114?childItemId=NMN9M95_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=99",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-half-pour-performance-jersey-polo-shirt-prod252710338?childItemId=NMN9L9Y_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=100",
            "https://www.neimanmarcus.com/en-bd/p/paige-mens-burke-tech-jersey-polo-shirt-prod252030247?childItemId=NMN9B0B_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=101",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-jubilee-performance-jersey-polo-shirt-prod248460290?childItemId=NMN8X8D_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=102",
            "https://www.neimanmarcus.com/en-bd/p/robert-graham-mens-archie-polo-shirt-w-contrast-detail-prod240190292?childItemId=NMN8448_42&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=103",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-roarin-20s-performance-jersey-polo-shirt-prod252710378?childItemId=NMN9LA0_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=104",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-striped-cuff-polo-shirt-prod247570101?childItemId=NMN8T42_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=105",
            "https://www.neimanmarcus.com/en-bd/p/balmain-mens-maxi-monogram-velvet-polo-shirt-prod251470102?childItemId=NMN99E9_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=106",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-crest-stretch-polo-shirt-prod247450036?childItemId=NMN8QAM_40&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=107",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-vintage-tile-performance-jersey-polo-shirt-prod252710188?childItemId=NMN9LA9_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=108",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-fordham-performance-jersey-polo-shirt-prod252710548?childItemId=NMN9LAH_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=109",
            "https://www.neimanmarcus.com/en-bd/p/rag-bone-mens-principal-jersey-polo-shirt-prod249940144?childItemId=NMN93S4_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=110",
            "https://www.neimanmarcus.com/en-bd/p/theory-mens-modal-jersey-polo-shirt-prod247280018?childItemId=NMN8RDD_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=111",
            "https://www.neimanmarcus.com/en-bd/p/kenzo-mens-pique-logo-polo-shirt-prod253130244?childItemId=NMN9P7C_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=112",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-lava-wash-jersey-polo-shirt-prod252710560?childItemId=NMN9LAM_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=113",
            "https://www.neimanmarcus.com/en-bd/p/loro-piana-2-button-regatta-polo-shirt-prod208090040?childItemId=NMN59LF_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=114",
            "https://www.neimanmarcus.com/en-bd/p/robert-graham-mens-beach-daze-cotton-french-terry-knit-polo-shirt-prod251630047?childItemId=NMN9A1Q_10&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=115",
            "https://www.neimanmarcus.com/en-bd/p/valentino-mens-pique-logo-polo-shirt-prod250300155?childItemId=NMN95PC_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=116",
            "https://www.neimanmarcus.com/en-bd/p/peter-millar-mens-crest-isle-striped-polo-shirt-prod247440033?childItemId=NMN8QAT_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=117",
            "https://www.neimanmarcus.com/en-bd/p/moncler-mens-classic-flag-trim-polo-shirt-prod242800326?childItemId=NMN8AXM_01&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=118",
            "https://www.neimanmarcus.com/en-bd/p/ralph-lauren-purple-label-mens-logo-polo-shirt-prod248810008?childItemId=NMN8S7H_&navpath=cat000000_cat82040732_cat14120827_cat13140748&page=0&position=119"
        ]

        for link in link_elements:
            yield scrapy.Request(url=link)

    def parse(self, response):
        print(response)
        """tom tailor scraping"""
        product_name = response.css(
            'span.Titlestyles__ProductName-fRiIcI bYyVMa::text').get()
        imgs = response.xpath(
            '//div[contains(@class, "Images__ImageWrapper-bwyNFg kUXuQF")]/picture/img/@src').getall()
        # imgs = list(dict.fromkeys(imgs))

        print('+----+' * 10)
        print(product_name)
        print(len(imgs))
        # print(imgs)
        print('+----+' * 10)

        # for img in range(len(imgs)):
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(
        #         f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img].replace('/560_745/', '/1654_2200/')}\n")
        # self.file_.close
