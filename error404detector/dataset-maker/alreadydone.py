# coding: utf-8

import pymongo
from databasetools.mongo import *
from systemtools.file import *
from systemtools.location import *
from systemtools.basics import *
from datatools.json import *
from datatools.csvreader import *
from webcrawler.utils import *
from webcrawler.browser import *
import sh
from webcrawler.error404.urls import *
import random


"""
invalid from Mathieu-49 https://www.wsj.com/articles/trump-to-sign-order-to-expand-health-insurance-options-for-self-insured-1507410483/jhgsdyuvsfd
invalid from Mathieu-49 http://www.couriermail.com.au/news/world/kim-jongun-october-10-holiday-the-latest-flash-point-that-could-lead-to-korean-war/news-story/ba6766aa4f1fd087a8e12f8f7e614c1e/jhgsdyuvsfd

invalid from Mathieu-49 https://news.google.fr//jhgsdyuvsfd

refused from Mathieu-49 http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city//jhgsdyuvsfd

invalid from Mathieu-49 https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp/jhgsdyuvsfd

refused from Mathieu-49 https://www.boston.com/sports/skiing/2017/11/07/its-really-happening-ski-season-starts-this-week-in-new-england/jhgsdyuvsfd

refused from Mathieu-49 http://www.koreaherald.com/view.php?ud=20171011000965/jhgsdyuvsfd

invalid from Mathieu-49 http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272/jhgsdyuvsfd

invalid from Mathieu-49 http://www.heraldsun.com.au/lifestyle/health/body-soul-daily/not-sleeping-best-insomnia-cure-could-be-ignoring-it/news-story/0734f87ce37af05d024619d4d9beaff5/jhgsdyuvsfd

refused from Mathieu-49 https://www.tvnz.co.nz/shows/the-orville/jhgsdyuvsfd

invalid from Mathieu-49 .com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f/jhgsdyuvsfd


"""


# TODO faire une url 404 meilleurs car ça redirige vers une page ok...

urlParser = URLParser()

# These url was done, its last urls in the 404 folder:
toDO = urlParser.strToUrls("""
invalid from Mathieu-49 https://www.wsj.com/articles/trump-to-sign-order-to-expand-health-insurance-options-for-self-insured-1507410483/jhgsdyuvsfd
invalid from Mathieu-49 http://www.couriermail.com.au/news/world/kim-jongun-october-10-holiday-the-latest-flash-point-that-could-lead-to-korean-war/news-story/ba6766aa4f1fd087a8e12f8f7e614c1e/jhgsdyuvsfd

invalid from Mathieu-49 https://news.google.fr//jhgsdyuvsfd

refused from Mathieu-49 http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city//jhgsdyuvsfd

invalid from Mathieu-49 https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp/jhgsdyuvsfd

refused from Mathieu-49 https://www.boston.com/sports/skiing/2017/11/07/its-really-happening-ski-season-starts-this-week-in-new-england/jhgsdyuvsfd

refused from Mathieu-49 http://www.koreaherald.com/view.php?ud=20171011000965/jhgsdyuvsfd

invalid from Mathieu-49 http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272/jhgsdyuvsfd

invalid from Mathieu-49 http://www.heraldsun.com.au/lifestyle/health/body-soul-daily/not-sleeping-best-insomnia-cure-could-be-ignoring-it/news-story/0734f87ce37af05d024619d4d9beaff5/jhgsdyuvsfd

refused from Mathieu-49 https://www.tvnz.co.nz/shows/the-orville/jhgsdyuvsfd

invalid from Mathieu-49 .com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f/jhgsdyuvsfd


""")

alreadyDone = []

alreadyDone2 = urlParser.strToUrls("""

error404 from Mathieu-49 http://www.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.bostonherald.com/news/local_politics/2017/11/liz_warren_cashes_in_on_herald_coverage/jhgsdyuvsfd
timeoutWithContent from Mathieu-49 http://www.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html/jhgsdyuvsfd
error404 from Mathieu-49 http://minnesota.cbslocal.com/2017/11/07/target-closings//jhgsdyuvsfd
error404 from Mathieu-49 http://www.thedailystar.net/country/international-crimes-tribunal-ict-1-bangladesh-government-reconstitutes-appointing-chairman-member-1474816/jhgsdyuvsfd
success from Mathieu-49 https://www.politico.com/story/2017/11/06/trumps-coal-backers-energy-power-rick-perry-244535/jhgsdyuvsfd
error404 from Mathieu-49 http://www.ctvnews.ca/world/q-a-catalonia-s-independence-push-explained-1.3624813/jhgsdyuvsfd
error404 from Mathieu-49 http://sanfrancisco.cbslocal.com/2017/11/07/exploding-washing-machine//jhgsdyuvsfd
error404 from Mathieu-49 https://www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796/jhgsdyuvsfd
success from Mathieu-49 https://www.timeslive.co.za/news/south-africa/2017-10-12-uncle-in-court-after-four-year-old-murdered-tossed-drain//jhgsdyuvsfd
error404 from Mathieu-49 https://www.irishtimes.com/news/crime-and-law/courts/high-court/anorexic-girl-missing-ireland-terribly-during-uk-treatment-1.3249795/jhgsdyuvsfd
success from Mathieu-49 http://www.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole/jhgsdyuvsfd


error404 from Mathieu-49 http://en.people.cn/n3/2017/1011/c90785-9278351.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.bbc.com/news/world-us-canada-41543631/jhgsdyuvsfd
error404 from Mathieu-49 http://www.ansa.it/english/news/2017/10/09/battisti-toasts-freedom-after-release-in-brazil_71cd224c-5156-41c4-a6eb-c89e8833d41f.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html/jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.co.uk/?country=UK/jhgsdyuvsfd
error404 from Mathieu-49 http://losangeles.cbslocal.com/2017/11/07/morey-boogie-board-inventor//jhgsdyuvsfd
success from Mathieu-49 http://nation.com.pk/national/11-Oct-2017/iranian-envoy-lauds-pakistan-s-efforts-for-regional-stability/jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.co.za/2017/10/08/zuma-has-dismissed-as-mischievous-claims-that-he-has-preferred-candidates-for-the-sabc-board_a_23236416/?utm_hp_ref=za-homepage/jhgsdyuvsfd
timeoutWithContent from Mathieu-49 http://www.dailymail.co.uk/tvshowbiz/article-4960002/Phillip-Schofield-enjoys-night-daughter-Ruby.html/jhgsdyuvsfd
success from Mathieu-49 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured/jhgsdyuvsfd
error404 from Mathieu-49 http://tampa.cbslocal.com/2017/11/07/ranch-dressing-keg-hidden-valley//jhgsdyuvsfd
error404 from Mathieu-49 http://www.nydailynews.com/new-york/nyc-crime/teen-reported-pimp-assault-disappearance-article-1.3617409/jhgsdyuvsfd

success from Mathieu-49 https://www.dawn.com/news/1363132/senate-adopts-resolution-against-disqualified-person-holding-party-office/jhgsdyuvsfd
success from Mathieu-49 https://www.stuff.co.nz/business/small-business/97687085/wellington-restaurant-closes-after-selling-two-illegal-wines-and-a-beer/jhgsdyuvsfd
timeoutWithContent from Mathieu-49 http://www.deccanherald.com/content/637343/mukul-roy-quits-trinamool-rajya.html/jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.com/entry/trump-judicial-nominee-abortion-rights_us_59d67a63e4b046f5ad96e117?ncid=inblnkushpmg00000009/jhgsdyuvsfd
success from Mathieu-49 http://decoetart.over-blog.com//jhgsdyuvsfd
success from Mathieu-49 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU/jhgsdyuvsfd
error404 from Mathieu-49 http://philadelphia.cbslocal.com/2017/11/07/serial-bank-robber-wanted-philly//jhgsdyuvsfd
error404 from Mathieu-49 https://www.seattletimes.com/seattle-news/politics/election-day-2017-live-updates-seattle-mayor-bellevue-king-county//jhgsdyuvsfd
error404 from Mathieu-49 http://www.dailystar.co.uk/showbiz/650687/Margot-Robbie-Hugh-Hefner-Playboy-film-Jared-Leto/jhgsdyuvsfd

success from Mathieu-49 https://www.businesspost.ie/news/ireland-feel-sharia-feel-justice-feel-freedom-feel-equality-399793/jhgsdyuvsfd
error404 from Mathieu-49 https://mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications/jhgsdyuvsfd
timeoutWithContent from Mathieu-49 http://www.thehindu.com/news/national/other-states/mns-activists-thrash-non-maharashtrian-workers-in-sangli/article19839494.ece/jhgsdyuvsfd
success from Mathieu-49 http://www.jamaicaobserver.com/news/senators-bid-farewell-to-golding-brown-burke_113570/jhgsdyuvsfd
success from Mathieu-49 http://www.shanghaidaily.com/metro/the-vip-gallery/Ying-Yong-Iowa-governor-talk-about-closer-ties/shdaily.shtml/jhgsdyuvsfd
error404 from Mathieu-49 http://www.manilatimes.net/comelec-chief-bautista-impeached/355884//jhgsdyuvsfd
success from Mathieu-49 https://www.washingtonpost.com/news/post-politics/wp/2017/10/08/trump-attacks-gop-sen-corker-didnt-have-the-guts-to-run-for-reelection/?hpid=hp_hp-top-table-main_pp-corker-1052am:homepage/story&utm_term=.363e157b0dfe/jhgsdyuvsfd
error404 from Mathieu-49 http://www.seattlepi.com/local/politics/article/Connely-Durkan-grabs-lead-for-Mayor-Mosqueda-12339465.php/jhgsdyuvsfd
success from Mathieu-49 http://www.npr.org/sections/thetwo-way/2017/11/05/562217575/multiple-casualties-reported-after-gunman-opens-fire-in-south-texas-church/jhgsdyuvsfd
error404 from Mathieu-49 http://ktla.com/2017/11/08/trump-arrives-in-beijing-for-high-stakes-visit-with-chinese-president//jhgsdyuvsfd
error404 from Mathieu-49 http://www.thejakartapost.com/academia/2017/10/11/commentary-papuan-women-youth-remind-us-of-second-class-citizens.html/jhgsdyuvsfd

error404 from Mathieu-49 http://gothamist.com/2017/11/02/west_side_bike_path_security.php/jhgsdyuvsfd
success from Mathieu-49 http://www.express.co.uk/news/royal/863798/Queen-Balmoral-summer-holiday-Craithie-church-Prince-Philip-England-Prince-Charles/jhgsdyuvsfd
error404 from Mathieu-49 https://www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks/jhgsdyuvsfd
error404 from Mathieu-49 http://www.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658//jhgsdyuvsfd
error404 from Mathieu-49 http://mexiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage//jhgsdyuvsfd
success from Mathieu-49 http://english.ahram.org.eg/NewsContentP/1/278663/Egypt/UPDATED-Rival-Palestinian-groups-Fatah-and-Hamas-r.aspx/jhgsdyuvsfd
error404 from Mathieu-49 http://www.laweekly.com/music/tokimonsta-battled-back-from-moyamoya-and-brain-surgery-to-make-the-excellent-lune-rouge-8827994/jhgsdyuvsfd
success from Mathieu-49 https://www.bangkokpost.com/news/general/1340223/king-of-bhutan-to-attend-ceremony/jhgsdyuvsfd
success from Mathieu-49 https://www.standardmedia.co.ke/article/2001256918/one-shot-two-run-over-by-motorist-as-anti-iebc-protests-turn-violent/jhgsdyuvsfd
error404 from Mathieu-49 http://economictimes.indiatimes.com/news/defence/how-india-plans-to-counter-chinas-salami-slicing-strategy/articleshow/61035843.cms/jhgsdyuvsfd
success from Mathieu-49 http://calgaryherald.com/sports/hockey/nhl/calgary-flames/flames-enter-haunted-honda-center-hoping-to-break-curse/jhgsdyuvsfd
error404 from Mathieu-49 http://www.philly.com/philly/sports/eagles/nfl-power-rankings-tamba-hali-philadelphia-eagles-dallas-cowboys-20171107.html/jhgsdyuvsfd
success from Mathieu-49 http://www.gulf-times.com/story/566982/Media-role-in-educating-people-about-dangers-of-dr/jhgsdyuvsfd
success from Mathieu-49 http://www.latimes.com/entertainment/movies/la-et-mn-harvey-weinstein-rise-fall-20171008-story.html/jhgsdyuvsfd


success from Mathieu-49 http://www.independent.co.uk/news/uk/politics/labour-tories-poll-latest-lead-jeremy-corbyn-theresa-may-pm-general-election-five-points-bmg-a7988166.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.itn.co.uk/press-releases/itn-productions-appoints-head-of-news//jhgsdyuvsfd
error404 from Mathieu-49 https://www.nytimes.com/2017/10/08/world/middleeast/isis-iraq-surrender.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=photo-spot-region&region=top-news&WT.nav=top-news/jhgsdyuvsfd
error404 from Mathieu-49 http://www.newsday.com/beta/long-island/crime/cops-man-offered-great-neck-estates-officer-drugs-money-1.14390657/jhgsdyuvsfd
error404 from Mathieu-49 http://www.dw.com/fr/les-vieux-frigos-europ%C3%A9ens-v%C3%A9ritables-polluants-en-afrique/a-40850876/jhgsdyuvsfd
success from Mathieu-49 https://elpais.com/elpais/2017/10/09/inenglish/1507534094_516802.html/jhgsdyuvsfd

error404 from Mathieu-49 http://www.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years//jhgsdyuvsfd

error404 from Mathieu-49 https://local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653/jhgsdyuvsfd
success from Mathieu-49 http://www.fijitimes.com/story.aspx?id=419425/jhgsdyuvsfd
error404 from Mathieu-49 https://korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.arabnews.com/node/1175921/middle-east/jhgsdyuvsfd
success from Mathieu-49 https://www.yahoo.com/news//jhgsdyuvsfd
error404 from Mathieu-49 http://www.deccanchronicle.com/nation/current-affairs/111017/solar-scam-pinarayi-vijayan-orders-vigilance-probe-against-oommen-chandy.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.france24.com/fr/20171009-france-qatar-egypte-elections-unesco-querelles-diplomatiques-azoulay-khattab/jhgsdyuvsfd
error404 from Mathieu-49 http://abc13.com/road-rage-victim-tells-abc13-what-led-to-shooting/2616988//jhgsdyuvsfd
error404 from Mathieu-49 https://www.nbcnewyork.com/news/local/Tammie-McCormick-Missing-New-York-Teenager-Cold-Case-456117483.html/jhgsdyuvsfd
error404 from Mathieu-49 http://boston.cbslocal.com/2017/11/07/shrewsbury-fatal-hit-and-run//jhgsdyuvsfd
error404 from Mathieu-49 https://thewest.com.au/news/wa/secret-harbour-crash-victim-will-continue-to-fight-in-rph-ng-b88624008z/jhgsdyuvsfd
success from Mathieu-49 http://www.skynews.com.au/news/top-stories/2017/10/09/nsw-government-moves-to-avoid-energy-crisis.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.pravdareport.com/news/world/americas/09-10-2017/138865-unmanned_orca_submarine-0//jhgsdyuvsfd
success from Mathieu-49 https://www.thesun.co.uk/news/4638007/trouble-for-theresa-as-labour-pull-ahead-of-tories-and-more-voters-prefer-jeremy-corbyn-as-pm//jhgsdyuvsfd
error404 from Mathieu-49 https://www.washingtontimes.com/news/2017/nov/7/schumer-predicts-dreamer-amnesty-will-be-part-year//jhgsdyuvsfd
error404 from Mathieu-49 http://www.jordantimes.com/news/region/fighters-raqqa-frontline-brace-final-showdown-daesh/jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.ca/2017/10/07/chrystia-freeland-gives-bleak-anti-globalization-history-book-to-nafta-partners_a_23235938/?utm_hp_ref=ca-homepage/jhgsdyuvsfd
error404 from Mathieu-49 http://www.latinamericanpost.com/index.php/identity/16486-the-left-has-not-failed/jhgsdyuvsfd
success from Mathieu-49 http://en.mercopress.com/2017/10/12/obama-officials-treated-special-relationship-with-britain-as-a-joke-and-liked-to-refer-to-falklands-as-malvinas/jhgsdyuvsfd
success from Mathieu-49 http://www.buenosairesherald.com/article/226417/explainer-maduro%E2%80%99s-constituent--assembly/jhgsdyuvsfd
error404 from Mathieu-49 https://www.kyivpost.com/ukraine-politics-2/lutsenko-says-russian-fsb-involved-kyiv-assassination-former-duma-lawmaker.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.hindustantimes.com/india-news/india-must-stick-to-fiscal-consolidation-says-pm-modi-s-economic-advisory-council/story-lMCT8eVsJBcrVx9j3sokwN.html/jhgsdyuvsfd
error404 from Mathieu-49 http://observer.com/2017/11/monday-night-football-ratings-nfl-lions-packers//jhgsdyuvsfd
error404 from Mathieu-49 http://www.monitor.co.ug/News/National/Kaweesi-murder-suspects-given-Shs80m-over-violation-rights/688334-4136524-w91uar/index.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.breitbart.com/texas/2017/11/07/texas-church-killer-escaped-mental-hospital-2012-says-report//jhgsdyuvsfd
error404 from Mathieu-49 http://www.nation.co.ke/news/Nasa-protests-in-Nairobi-city-centre-Fred-Matiangi/1056-4136704-7tc9a1z/index.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.mirror.co.uk/news/world-news/massive-fire-erupts-moscow-market-11308842/jhgsdyuvsfd
success from Mathieu-49 https://themoscowtimes.com/news/senators-look-to-cut-us-media-numbers-in-russia-59209/jhgsdyuvsfd
success from Mathieu-49 https://news.google.com/news//jhgsdyuvsfd
success from Mathieu-49 http://montrealgazette.com/news/local-news/thanksgiving-whats-open-and-closed-on-monday/jhgsdyuvsfd
error404 from Mathieu-49 https://www.cbsnews.com/news/how-facebook-ads-helped-elect-trump//jhgsdyuvsfd
error404 from Mathieu-49 http://www.herald.ie/news/crime-lord-gilligans-seized-house-could-be-used-to-help-homeless-36208115.html/jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.fr/2017/10/08/seminaire-gouvernemental-pourquoi-edouard-philippe-reunit-son-equipe-a-matignon-ce-dimanche_a_23236296/?utm_hp_ref=fr-homepage/jhgsdyuvsfd
success from Mathieu-49 http://www.chicagotribune.com/sports/chicagomarathon/ct-tirunesh-dibaba-womens-chicago-marathon-20171008-story.html/jhgsdyuvsfd
error404 from Mathieu-49 http://www.radionz.co.nz/news/world/341193/trump-ties-border-wall-to-dreamer-plan/jhgsdyuvsfd
success from Mathieu-49 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play/jhgsdyuvsfd
success from Mathieu-49 https://www.odt.co.nz/regions/southland/three-killed-southland-crash/jhgsdyuvsfd
success from Mathieu-49 https://www.praguepost.com/prague-news/marketing-festival-comes-to-prague-on-november-9th/jhgsdyuvsfd
error404 from Mathieu-49 http://www.caribbeannews.com//jhgsdyuvsfd
error404 from Mathieu-49 http://news.kuwaittimes.net/website/zain-finalizes-telecoms-tower-deal-first-kind-region//jhgsdyuvsfd
error404 from Mathieu-49 https://wtop.com/virginia/2017/11/democrats-come-close-to-retaking-virginia-house//jhgsdyuvsfd

error404 from Mathieu-49 https://www.vanguardngr.com/2017/10/senate-begins-consideration-buharis-5-5bn-loan//jhgsdyuvsfd
error404 from Mathieu-49 https://chicago.suntimes.com/chicago-politics/writer-accuses-rev-jesse-jackson-of-sexual-harassment//jhgsdyuvsfd
success from Mathieu-49 https://www.businesslive.co.za/bd/companies/2017-10-12-reserve-bank-probing-bank-of-baroda-after-outa-allegations//jhgsdyuvsfd
error404 from Mathieu-49 http://edition.cnn.com/2017/10/07/us/las-vegas-shooting-investigation/index.html/jhgsdyuvsfd
success from Mathieu-49 http://riotimesonline.com/brazil-news/rio-politics/armed-forces-return-in-search-operation-of-rios-rocinha-favela//jhgsdyuvsfd
success from Mathieu-49 http://www.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp/jhgsdyuvsfd
error404 from Mathieu-49 https://timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms/jhgsdyuvsfd
success from Mathieu-49 https://www.usatoday.com/story/news/politics/2017/10/08/trump-blasts-sen-bob-corker-negative-voice-gop-agenda/744071001//jhgsdyuvsfd
error404 from Mathieu-49 http://sunnewsonline.com/fish-out-assassins-of-ex-head-of-service-group-urges-lalong//jhgsdyuvsfd
error404 from Mathieu-49 http://jamaica-gleaner.com/article/lead-stories/20171012/transport-authority-spends-millions-secure-rat-infested-building/jhgsdyuvsfd

success from Mathieu-49 http://www.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini/jhgsdyuvsfd
success from Mathieu-49 http://www.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12/jhgsdyuvsfd
error404 from Mathieu-49 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97/jhgsdyuvsfd
success from Mathieu-49 http://www.warsawvoice.pl/WVpage/pages/article.php/40189/news/jhgsdyuvsfd
error404 from Mathieu-49 http://punchng.com/new-york-police-reopens-2004-weinstein-assault-case//jhgsdyuvsfd
success from Mathieu-49 http://www.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450/jhgsdyuvsfd
error404 from Mathieu-49 http://www.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee//jhgsdyuvsfd
error404 from Mathieu-49 http://dfw.cbslocal.com/2017/11/07/denton-paper-ballots//jhgsdyuvsfd
error404 from Mathieu-49 http://www.cubanews.acn.cu/cuba/7376-eusebio-leal-calls-to-preserve-unity-of-the-nation/jhgsdyuvsfd
error404 from Mathieu-49 http://www.irishexaminer.com/examviral/is-this-cork-shop-notice-the-most-irish-sign-ever-809163.html/jhgsdyuvsfd
error404 from Mathieu-49 http://washington.cbslocal.com/2017/11/06/caps-overcome-2-goal-deficit-win-in-ot//jhgsdyuvsfd
success from Mathieu-49 http://www.foxnews.com/us/2017/10/08/vice-president-mike-pence-leaves-colts-49ers-game-after-players-reportedly-kneel.html/jhgsdyuvsfd
error404 from Mathieu-49 http://indianexpress.com/article/business/economic-advisory-council-identifies-10-key-areas-to-focus-on-critical-policy-interventions-4885067//jhgsdyuvsfd
success from Mathieu-49 http://abcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532/jhgsdyuvsfd
error404 from Mathieu-49 http://www.palestinechronicle.com/the-balfour-declaration-destroyed-palestine-not-the-palestinian-people//jhgsdyuvsfd
error404 from Mathieu-49 http://www.thenational.com.pg/lupari-wants-focus-services//jhgsdyuvsfd
error404 from Mathieu-49 http://www.egyptindependent.com/valuable-wild-salmon-fishery-world-trump-administration-become-mine//jhgsdyuvsfd
error404 from Mathieu-49 http://www.sfchronicle.com/business/article/California-could-ban-gasoline-cars-if-12259588.php/jhgsdyuvsfd
error404 from Mathieu-49 http://www.denverpost.com/2017/10/08/bob-corker-donald-trump-adult-day-care//jhgsdyuvsfd
success from Mathieu-49 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead/jhgsdyuvsfd
success from Mathieu-49 http://www.newsnow.co.uk/h//jhgsdyuvsfd

error404 from Mathieu-49 http://chicago.cbslocal.com/2017/11/07/felony-franks-closed//jhgsdyuvsfd
success from Mathieu-49 https://fr.news.yahoo.com//jhgsdyuvsfd
success from Mathieu-49 http://www.chicagotribune.com/news/nationworld/ct-texas-church-shooting-witness-accounts-20171107-story.html/jhgsdyuvsfd
error404 from Mathieu-49 https://guardian.ng/news/frances-macron-launches-second-round-of-reforms//jhgsdyuvsfd
error404 from Mathieu-49 http://www.mercurynews.com/2017/11/07/brainstorming-the-bay-area-housing-crisis-thousands-sign-up-for-community-wide-conversation//jhgsdyuvsfd
success from Mathieu-49 http://www.reuters.com/article/us-texas-shooting/texas-gunmans-in-laws-sometimes-attended-church-sheriff-says-idUSKBN1D510F?feedType=RSS&feedName=domesticNews/jhgsdyuvsfd
error404 from Mathieu-49 http://www.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219/jhgsdyuvsfd
error404 from Mathieu-49 http://www.newsweek.com/new-york-elections-what-constitutional-convention-why-should-voters-care-703777/jhgsdyuvsfd
success from Mathieu-49 https://beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833//jhgsdyuvsfd
error404 from Mathieu-49 https://www.theguardian.com/world/2017/oct/08/catalonia-spain-prime-minister-refuses-rule-out-suspending-autonomy/jhgsdyuvsfd
error404 from Mathieu-49 https://www.thetimes.co.uk/edition/news/theresa-may-plots-to-demote-boris-johnson-in-reshuffle-fn36vztvd/jhgsdyuvsfd
timeoutWithContent from Mathieu-49 http://theprovince.com/sports/hockey/nhl/vancouver-canucks/canucks-derek-dorsetts-pride-pace-pesky-play-spark-shutdown-winger/jhgsdyuvsfd
error404 from Mathieu-49 http://detroit.cbslocal.com/2017/11/07/oreilly-auto-parts-murder-arrests-update//jhgsdyuvsfd
success from Mathieu-49 http://www.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage/jhgsdyuvsfd
error404 from Mathieu-49 http://news.sky.com/story/karen-bradley-insists-more-than-90-of-tory-mps-back-theresa-may-11072357/jhgsdyuvsfd
success from Mathieu-49 http://vancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3/jhgsdyuvsfd
error404 from Mathieu-49 http://newyork.cbslocal.com/2017/11/07/roy-halladay-plane-crash//jhgsdyuvsfd


""")

alreadyDoneOk = urlParser.strToUrls("""

success from Jean-Claude-98 http://www.huffingtonpost.ca/2017/10/07/chrystia-freeland-gives-bleak-anti-globalization-history-book-to-nafta-partners_a_23235938/?utm_hp_ref=ca-homepage
error404 from Jean-Claude-98 http://www.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years/
success from Jean-Claude-98 http://www.reuters.com/article/us-texas-shooting/texas-gunmans-in-laws-sometimes-attended-church-sheriff-says-idUSKBN1D510F?feedType=RSS&feedName=domesticNews
error404 from Jean-Claude-98 http://www.couriermail.com.au/news/world/kim-jongun-october-10-holiday-the-latest-flash-point-that-could-lead-to-korean-war/news-story/ba6766aa4f1fd087a8e12f8f7e614c1e
success from Jean-Claude-98 http://www.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage
timeoutWithContent from Jean-Claude-98 http://www.huffingtonpost.co.uk/?country=UK
success from Jean-Claude-98 http://news.kuwaittimes.net/website/zain-finalizes-telecoms-tower-deal-first-kind-region/
success from Jean-Claude-98 http://www.thehindu.com/news/national/other-states/mns-activists-thrash-non-maharashtrian-workers-in-sangli/article19839494.ece
success from Jean-Claude-98 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
success from Jean-Claude-98 http://www.huffingtonpost.fr/2017/10/08/seminaire-gouvernemental-pourquoi-edouard-philippe-reunit-son-equipe-a-matignon-ce-dimanche_a_23236296/?utm_hp_ref=fr-homepage
error404 from Jean-Claude-98 https://thewest.com.au/news/wa/secret-harbour-crash-victim-will-continue-to-fight-in-rph-ng-b88624008z
error404 from Jean-Claude-98 http://philadelphia.cbslocal.com/2017/11/07/serial-bank-robber-wanted-philly/
success from Jean-Claude-98 http://www.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450
success from Jean-Claude-98 http://www.jordantimes.com/news/region/fighters-raqqa-frontline-brace-final-showdown-daesh
error404 from Jean-Claude-98 http://dfw.cbslocal.com/2017/11/07/denton-paper-ballots/
success from Jean-Claude-98 https://elpais.com/elpais/2017/10/09/inenglish/1507534094_516802.html
error404 from Jean-Claude-98 https://www.irishtimes.com/news/crime-and-law/courts/high-court/anorexic-girl-missing-ireland-terribly-during-uk-treatment-1.3249795
success from Jean-Claude-98 https://www.stuff.co.nz/business/small-business/97687085/wellington-restaurant-closes-after-selling-two-illegal-wines-and-a-beer
timeoutWithContent from Jean-Claude-98 http://www.bostonherald.com/news/local_politics/2017/11/liz_warren_cashes_in_on_herald_coverage
error404 from Jean-Claude-98 https://mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications
success from Jean-Claude-98 http://edition.cnn.com/2017/10/07/us/las-vegas-shooting-investigation/index.html
error404 from Jean-Claude-98 http://www.buenosairesherald.com/article/226417/explainer-maduro%E2%80%99s-constituent--assembly
success from Jean-Claude-98 http://punchng.com/new-york-police-reopens-2004-weinstein-assault-case/
success from Jean-Claude-98 https://timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms
success from Jean-Claude-98 http://www.radionz.co.nz/news/world/341193/trump-ties-border-wall-to-dreamer-plan
success from Jean-Claude-98 https://www.standardmedia.co.ke/article/2001256918/one-shot-two-run-over-by-motorist-as-anti-iebc-protests-turn-violent
error404 from Jean-Claude-98 http://minnesota.cbslocal.com/2017/11/07/target-closings/
success from Jean-Claude-98 http://www.bbc.com/news/world-us-canada-41543631
success from Jean-Claude-98 http://www.fijitimes.com/story.aspx?id=419425
success from Jean-Claude-98 http://indianexpress.com/article/business/economic-advisory-council-identifies-10-key-areas-to-focus-on-critical-policy-interventions-4885067/
success from Jean-Claude-98 http://www.thenational.com.pg/lupari-wants-focus-services/
success from Jean-Claude-98 http://www.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12
success from Jean-Claude-98 http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272
success from Jean-Claude-98 https://www.theguardian.com/world/2017/oct/08/catalonia-spain-prime-minister-refuses-rule-out-suspending-autonomy
success from Jean-Claude-98 http://www.irishexaminer.com/examviral/is-this-cork-shop-notice-the-most-irish-sign-ever-809163.html
success from Jean-Claude-98 https://www.tvnz.co.nz/shows/the-orville
error404 from Jean-Claude-98 https://www.nytimes.com/2017/10/08/world/middleeast/isis-iraq-surrender.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=photo-spot-region&region=top-news&WT.nav=top-news
success from Jean-Claude-98 http://www.newsday.com/beta/long-island/crime/cops-man-offered-great-neck-estates-officer-drugs-money-1.14390657
success from Jean-Claude-98 http://www.npr.org/sections/thetwo-way/2017/11/05/562217575/multiple-casualties-reported-after-gunman-opens-fire-in-south-texas-church
success from Jean-Claude-98 http://www.sfchronicle.com/business/article/California-could-ban-gasoline-cars-if-12259588.php
success from Jean-Claude-98 https://www.boston.com/sports/skiing/2017/11/07/its-really-happening-ski-season-starts-this-week-in-new-england
success from Jean-Claude-98 http://www.caribbeannews.com/
success from Jean-Claude-98 http://calgaryherald.com/sports/hockey/nhl/calgary-flames/flames-enter-haunted-honda-center-hoping-to-break-curse
success from Jean-Claude-98 http://en.mercopress.com/2017/10/12/obama-officials-treated-special-relationship-with-britain-as-a-joke-and-liked-to-refer-to-falklands-as-malvinas
error404 from Jean-Claude-98 http://sanfrancisco.cbslocal.com/2017/11/07/exploding-washing-machine/
success from Jean-Claude-98 https://www.seattletimes.com/seattle-news/politics/election-day-2017-live-updates-seattle-mayor-bellevue-king-county/
success from Jean-Claude-98 http://www.foxnews.com/us/2017/10/08/vice-president-mike-pence-leaves-colts-49ers-game-after-players-reportedly-kneel.html
error404 from Jean-Claude-98 http://ktla.com/2017/11/08/trump-arrives-in-beijing-for-high-stakes-visit-with-chinese-president/
success from Jean-Claude-98 http://abc13.com/road-rage-victim-tells-abc13-what-led-to-shooting/2616988/
success from Jean-Claude-98 http://www.nydailynews.com/new-york/nyc-crime/teen-reported-pimp-assault-disappearance-article-1.3617409
error404 from Jean-Claude-98 https://beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833/
success from Jean-Claude-98 http://www.manilatimes.net/comelec-chief-bautista-impeached/355884/
success from Jean-Claude-98 http://www.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html
success from Jean-Claude-98 http://www.ctvnews.ca/world/q-a-catalonia-s-independence-push-explained-1.3624813
success from Jean-Claude-98 http://observer.com/2017/11/monday-night-football-ratings-nfl-lions-packers/
success from Jean-Claude-98 https://www.nbcnewyork.com/news/local/Tammie-McCormick-Missing-New-York-Teenager-Cold-Case-456117483.html
success from Jean-Claude-98 http://montrealgazette.com/news/local-news/thanksgiving-whats-open-and-closed-on-monday
success from Jean-Claude-98 http://www.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee/
error404 from Jean-Claude-98 http://www.cubanews.acn.cu/cuba/7376-eusebio-leal-calls-to-preserve-unity-of-the-nation
error404 from Jean-Claude-98 https://chicago.suntimes.com/chicago-politics/writer-accuses-rev-jesse-jackson-of-sexual-harassment/
success from Jean-Claude-98 https://korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html
error404 from Jean-Claude-98 http://boston.cbslocal.com/2017/11/07/shrewsbury-fatal-hit-and-run/
success from Jean-Claude-98 http://www.seattlepi.com/local/politics/article/Connely-Durkan-grabs-lead-for-Mayor-Mosqueda-12339465.php
success from Jean-Claude-98 http://www.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219
error404 from Jean-Claude-98 http://detroit.cbslocal.com/2017/11/07/oreilly-auto-parts-murder-arrests-update/
success from Jean-Claude-98 https://www.thetimes.co.uk/edition/news/theresa-may-plots-to-demote-boris-johnson-in-reshuffle-fn36vztvd
success from Jean-Claude-98 http://riotimesonline.com/brazil-news/rio-politics/armed-forces-return-in-search-operation-of-rios-rocinha-favela/
error404 from Jean-Claude-98 http://chicago.cbslocal.com/2017/11/07/felony-franks-closed/
success from Jean-Claude-98 http://sunnewsonline.com/fish-out-assassins-of-ex-head-of-service-group-urges-lalong/
success from Jean-Claude-98 https://www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796
success from Jean-Claude-98 https://www.dawn.com/news/1363132/senate-adopts-resolution-against-disqualified-person-holding-party-office
success from Jean-Claude-98 http://www.express.co.uk/news/royal/863798/Queen-Balmoral-summer-holiday-Craithie-church-Prince-Philip-England-Prince-Charles
success from Jean-Claude-98 http://www.shanghaidaily.com/metro/the-vip-gallery/Ying-Yong-Iowa-governor-talk-about-closer-ties/shdaily.shtml
error404 from Jean-Claude-98 http://www.heraldsun.com.au/lifestyle/health/body-soul-daily/not-sleeping-best-insomnia-cure-could-be-ignoring-it/news-story/0734f87ce37af05d024619d4d9beaff5
success from Jean-Claude-98 http://www.dw.com/fr/les-vieux-frigos-europ%C3%A9ens-v%C3%A9ritables-polluants-en-afrique/a-40850876
error404 from Jean-Claude-98 http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/
error404 from Jean-Claude-98 https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp
success from Jean-Claude-98 http://nation.com.pk/national/11-Oct-2017/iranian-envoy-lauds-pakistan-s-efforts-for-regional-stability
success from Jean-Claude-98 https://www.thesun.co.uk/news/4638007/trouble-for-theresa-as-labour-pull-ahead-of-tories-and-more-voters-prefer-jeremy-corbyn-as-pm/
success from Jean-Claude-98 http://www.monitor.co.ug/News/National/Kaweesi-murder-suspects-given-Shs80m-over-violation-rights/688334-4136524-w91uar/index.html
success from Jean-Claude-98 https://www.odt.co.nz/regions/southland/three-killed-southland-crash
success from Jean-Claude-98 http://www.latimes.com/entertainment/movies/la-et-mn-harvey-weinstein-rise-fall-20171008-story.html
success from Jean-Claude-98 http://www.gulf-times.com/story/566982/Media-role-in-educating-people-about-dangers-of-dr
success from Jean-Claude-98 http://www.nation.co.ke/news/Nasa-protests-in-Nairobi-city-centre-Fred-Matiangi/1056-4136704-7tc9a1z/index.html
success from Jean-Claude-98 http://www.hindustantimes.com/india-news/india-must-stick-to-fiscal-consolidation-says-pm-modi-s-economic-advisory-council/story-lMCT8eVsJBcrVx9j3sokwN.html
success from Jean-Claude-98 http://www.thedailystar.net/country/international-crimes-tribunal-ict-1-bangladesh-government-reconstitutes-appointing-chairman-member-1474816
success from Jean-Claude-98 http://www.itn.co.uk/press-releases/itn-productions-appoints-head-of-news/
error404 from Jean-Claude-98 http://news.sky.com/story/karen-bradley-insists-more-than-90-of-tory-mps-back-theresa-may-11072357
success from Jean-Claude-98 http://www.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp
success from Jean-Claude-98 http://www.thejakartapost.com/academia/2017/10/11/commentary-papuan-women-youth-remind-us-of-second-class-citizens.html
success from Jean-Claude-98 https://wtop.com/virginia/2017/11/democrats-come-close-to-retaking-virginia-house/
success from Jean-Claude-98 http://www.skynews.com.au/news/top-stories/2017/10/09/nsw-government-moves-to-avoid-energy-crisis.html
success from Jean-Claude-98 http://www.herald.ie/news/crime-lord-gilligans-seized-house-could-be-used-to-help-homeless-36208115.html
error404 from Jean-Claude-98 http://www.arabnews.com/node/1175921/middle-east
error404 from Jean-Claude-98 http://gothamist.com/2017/11/02/west_side_bike_path_security.php
success from Jean-Claude-98 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
timeoutWithContent from Jean-Claude-98 http://www.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html
success from Jean-Claude-98 https://www.timeslive.co.za/news/south-africa/2017-10-12-uncle-in-court-after-four-year-old-murdered-tossed-drain/
timeoutWithContent from Jean-Claude-98 http://www.huffingtonpost.com/entry/trump-judicial-nominee-abortion-rights_us_59d67a63e4b046f5ad96e117?ncid=inblnkushpmg00000009
error404 from Jean-Claude-98 http://washington.cbslocal.com/2017/11/06/caps-overcome-2-goal-deficit-win-in-ot/
success from Jean-Claude-98 http://www.france24.com/fr/20171009-france-qatar-egypte-elections-unesco-querelles-diplomatiques-azoulay-khattab
error404 from Jean-Claude-98 http://losangeles.cbslocal.com/2017/11/07/morey-boogie-board-inventor/
error404 from Jean-Claude-98 https://www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks
success from Jean-Claude-98 http://www.koreaherald.com/view.php?ud=20171011000965
success from Jean-Claude-98 http://www.deccanherald.com/content/637343/mukul-roy-quits-trinamool-rajya.html
success from Jean-Claude-98 https://themoscowtimes.com/news/senators-look-to-cut-us-media-numbers-in-russia-59209
success from Jean-Claude-98 http://vancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3
success from Jean-Claude-98 http://www.jamaicaobserver.com/news/senators-bid-farewell-to-golding-brown-burke_113570
success from Jean-Claude-98 http://theprovince.com/sports/hockey/nhl/vancouver-canucks/canucks-derek-dorsetts-pride-pace-pesky-play-spark-shutdown-winger
error404 from Jean-Claude-98 http://newyork.cbslocal.com/2017/11/07/roy-halladay-plane-crash/
success from Jean-Claude-98 http://www.egyptindependent.com/valuable-wild-salmon-fishery-world-trump-administration-become-mine/
timeoutWithContent from Jean-Claude-98 https://local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653
success from Jean-Claude-98 http://www.mirror.co.uk/news/world-news/massive-fire-erupts-moscow-market-11308842
success from Jean-Claude-98 https://www.usatoday.com/story/news/politics/2017/10/08/trump-blasts-sen-bob-corker-negative-voice-gop-agenda/744071001/
success from Jean-Claude-98 http://www.laweekly.com/music/tokimonsta-battled-back-from-moyamoya-and-brain-surgery-to-make-the-excellent-lune-rouge-8827994
success from Jean-Claude-98 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
success from Jean-Claude-98 http://www.mercurynews.com/2017/11/07/brainstorming-the-bay-area-housing-crisis-thousands-sign-up-for-community-wide-conversation/
success from Jean-Claude-98 http://www.ansa.it/english/news/2017/10/09/battisti-toasts-freedom-after-release-in-brazil_71cd224c-5156-41c4-a6eb-c89e8833d41f.html
error404 from Jean-Claude-98 http://en.people.cn/n3/2017/1011/c90785-9278351.html
success from Jean-Claude-98 https://www.cbsnews.com/news/how-facebook-ads-helped-elect-trump/
success from Jean-Claude-98 https://www.bangkokpost.com/news/general/1340223/king-of-bhutan-to-attend-ceremony
timeoutWithContent from Jean-Claude-98 http://www.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html
success from Jean-Claude-98 http://www.chicagotribune.com/sports/chicagomarathon/ct-tirunesh-dibaba-womens-chicago-marathon-20171008-story.html
timeoutWithContent from Jean-Claude-98 http://mexiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage/
success from Jean-Claude-98 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
success from Jean-Claude-98 http://www.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini
success from Jean-Claude-98 https://www.washingtontimes.com/news/2017/nov/7/schumer-predicts-dreamer-amnesty-will-be-part-year/
success from Jean-Claude-98 https://www.politico.com/story/2017/11/06/trumps-coal-backers-energy-power-rick-perry-244535
success from Jean-Claude-98 http://abcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
error404 from Jean-Claude-98 http://www.philly.com/philly/sports/eagles/nfl-power-rankings-tamba-hali-philadelphia-eagles-dallas-cowboys-20171107.html
success from Jean-Claude-98 http://economictimes.indiatimes.com/news/defence/how-india-plans-to-counter-chinas-salami-slicing-strategy/articleshow/61035843.cms
success from Jean-Claude-98 http://www.newsweek.com/new-york-elections-what-constitutional-convention-why-should-voters-care-703777
success from Jean-Claude-98 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
success from Jean-Claude-98 https://www.wsj.com/articles/trump-to-sign-order-to-expand-health-insurance-options-for-self-insured-1507410483
success from Jean-Claude-98 http://www.denverpost.com/2017/10/08/bob-corker-donald-trump-adult-day-care/
timeoutWithContent from Jean-Claude-98 http://www.independent.co.uk/news/uk/politics/labour-tories-poll-latest-lead-jeremy-corbyn-theresa-may-pm-general-election-five-points-bmg-a7988166.html
error404 from Jean-Claude-98 http://www.adelaidenow.com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f
success from Jean-Claude-98 http://www.latinamericanpost.com/index.php/identity/16486-the-left-has-not-failed
success from Jean-Claude-98 http://www.chicagotribune.com/news/nationworld/ct-texas-church-shooting-witness-accounts-20171107-story.html
success from Jean-Claude-98 http://www.newsnow.co.uk/h/
success from Jean-Claude-98 https://www.businesslive.co.za/bd/companies/2017-10-12-reserve-bank-probing-bank-of-baroda-after-outa-allegations/
success from Jean-Claude-98 https://www.vanguardngr.com/2017/10/senate-begins-consideration-buharis-5-5bn-loan/
success from Jean-Claude-98 https://www.praguepost.com/prague-news/marketing-festival-comes-to-prague-on-november-9th
error404 from Jean-Claude-98 http://jamaica-gleaner.com/article/lead-stories/20171012/transport-authority-spends-millions-secure-rat-infested-building
success from Jean-Claude-98 https://guardian.ng/news/frances-macron-launches-second-round-of-reforms/
success from Jean-Claude-98 http://www.deccanchronicle.com/nation/current-affairs/111017/solar-scam-pinarayi-vijayan-orders-vigilance-probe-against-oommen-chandy.html
timeoutWithContent from Jean-Claude-98 http://www.dailymail.co.uk/tvshowbiz/article-4960002/Phillip-Schofield-enjoys-night-daughter-Ruby.html
success from Jean-Claude-98 https://www.washingtonpost.com/news/post-politics/wp/2017/10/08/trump-attacks-gop-sen-corker-didnt-have-the-guts-to-run-for-reelection/?hpid=hp_hp-top-table-main_pp-corker-1052am:homepage/story&utm_term=.363e157b0dfe
success from Jean-Claude-98 https://www.businesspost.ie/news/ireland-feel-sharia-feel-justice-feel-freedom-feel-equality-399793
success from Jean-Claude-98 http://www.palestinechronicle.com/the-balfour-declaration-destroyed-palestine-not-the-palestinian-people/
error404 from Jean-Claude-98 http://tampa.cbslocal.com/2017/11/07/ranch-dressing-keg-hidden-valley/
success from Jean-Claude-98 http://www.warsawvoice.pl/WVpage/pages/article.php/40189/news
success from Jean-Claude-98 http://www.dailystar.co.uk/showbiz/650687/Margot-Robbie-Hugh-Hefner-Playboy-film-Jared-Leto
success from Jean-Claude-98 http://www.huffingtonpost.co.za/2017/10/08/zuma-has-dismissed-as-mischievous-claims-that-he-has-preferred-candidates-for-the-sabc-board_a_23236416/?utm_hp_ref=za-homepage
success from Jean-Claude-98 http://www.breitbart.com/texas/2017/11/07/texas-church-killer-escaped-mental-hospital-2012-says-report/
success from Jean-Claude-98 http://www.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole
success from Jean-Claude-98 http://english.ahram.org.eg/NewsContentP/1/278663/Egypt/UPDATED-Rival-Palestinian-groups-Fatah-and-Hamas-r.aspx

success from Yannis-18 https://www.kyivpost.com/ukraine-politics-2/lutsenko-says-russian-fsb-involved-kyiv-assassination-former-duma-lawmaker.html
error404 from Yannis-18 http://www.pravdareport.com/news/world/americas/09-10-2017/138865-unmanned_orca_submarine-0/
success from Yannis-18 http://www.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658/


""")

alreadyDone_old = urlParser.strToUrls("""

success from Annick-73 http://www.koreaherald.com/view.php?ud=20171011000965
timeoutWithContent from Annick-73 http://philadelphia.cbslocal.com/2017/11/07/serial-bank-robber-wanted-philly/
success from Annick-73 https://www.dawn.com/news/1363132/senate-adopts-resolution-against-disqualified-person-holding-party-office
success from Annick-73 http://www.newsday.com/beta/long-island/crime/cops-man-offered-great-neck-estates-officer-drugs-money-1.14390657
success from Annick-73 http://www.chicagotribune.com/sports/chicagomarathon/ct-tirunesh-dibaba-womens-chicago-marathon-20171008-story.html
success from Annick-73 http://english.ahram.org.eg/NewsContentP/1/278663/Egypt/UPDATED-Rival-Palestinian-groups-Fatah-and-Hamas-r.aspx
success from Annick-73 http://www.huffingtonpost.com/entry/trump-judicial-nominee-abortion-rights_us_59d67a63e4b046f5ad96e117?ncid=inblnkushpmg00000009
success from Annick-73 http://www.thehindu.com/news/national/other-states/mns-activists-thrash-non-maharashtrian-workers-in-sangli/article19839494.ece
success from Annick-73 http://www.shanghaidaily.com/metro/the-vip-gallery/Ying-Yong-Iowa-governor-talk-about-closer-ties/shdaily.shtml
success from Annick-73 http://www.latinamericanpost.com/index.php/identity/16486-the-left-has-not-failed
success from Annick-73 http://www.irishexaminer.com/examviral/is-this-cork-shop-notice-the-most-irish-sign-ever-809163.html
success from Annick-73 https://guardian.ng/news/frances-macron-launches-second-round-of-reforms/
success from Annick-73 http://www.monitor.co.ug/News/National/Kaweesi-murder-suspects-given-Shs80m-over-violation-rights/688334-4136524-w91uar/index.html
success from Annick-73 https://www.timeslive.co.za/news/south-africa/2017-10-12-uncle-in-court-after-four-year-old-murdered-tossed-drain/
timeoutWithContent from Annick-73 http://sanfrancisco.cbslocal.com/2017/11/07/exploding-washing-machine/
success from Annick-73 http://www.thedailystar.net/country/international-crimes-tribunal-ict-1-bangladesh-government-reconstitutes-appointing-chairman-member-1474816
success from Annick-73 https://www.washingtonpost.com/news/post-politics/wp/2017/10/08/trump-attacks-gop-sen-corker-didnt-have-the-guts-to-run-for-reelection/?hpid=hp_hp-top-table-main_pp-corker-1052am:homepage/story&utm_term=.363e157b0dfe
error404 from Annick-73 http://en.people.cn/n3/2017/1011/c90785-9278351.html
success from Annick-73 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
success from Annick-73 http://theprovince.com/sports/hockey/nhl/vancouver-canucks/canucks-derek-dorsetts-pride-pace-pesky-play-spark-shutdown-winger
success from Annick-73 https://www.cbsnews.com/news/how-facebook-ads-helped-elect-trump/
success from Annick-73 http://www.mirror.co.uk/news/world-news/massive-fire-erupts-moscow-market-11308842
timeoutWithContent from Annick-73 http://www.nydailynews.com/new-york/nyc-crime/teen-reported-pimp-assault-disappearance-article-1.3617409
success from Annick-73 http://edition.cnn.com/2017/10/07/us/las-vegas-shooting-investigation/index.html
success from Annick-73 https://www.boston.com/sports/skiing/2017/11/07/its-really-happening-ski-season-starts-this-week-in-new-england
success from Annick-73 https://www.praguepost.com/prague-news/marketing-festival-comes-to-prague-on-november-9th
success from Annick-73 https://www.politico.com/story/2017/11/06/trumps-coal-backers-energy-power-rick-perry-244535
success from Annick-73 https://www.yahoo.com/news/
timeoutWithContent from Annick-73 https://www.nytimes.com/2017/10/08/world/middleeast/isis-iraq-surrender.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=photo-spot-region&region=top-news&WT.nav=top-news
success from Annick-73 http://www.huffingtonpost.co.za/2017/10/08/zuma-has-dismissed-as-mischievous-claims-that-he-has-preferred-candidates-for-the-sabc-board_a_23236416/?utm_hp_ref=za-homepage
success from Annick-73 http://www.dailystar.co.uk/showbiz/650687/Margot-Robbie-Hugh-Hefner-Playboy-film-Jared-Leto
success from Annick-73 http://www.fijitimes.com/story.aspx?id=419425
success from Annick-73 http://www.newsnow.co.uk/h/
success from Annick-73 http://www.chicagotribune.com/news/nationworld/ct-texas-church-shooting-witness-accounts-20171107-story.html
success from Annick-73 http://economictimes.indiatimes.com/news/defence/how-india-plans-to-counter-chinas-salami-slicing-strategy/articleshow/61035843.cms
success from Annick-73 https://www.wsj.com/articles/trump-to-sign-order-to-expand-health-insurance-options-for-self-insured-1507410483
success from Annick-73 http://news.kuwaittimes.net/website/zain-finalizes-telecoms-tower-deal-first-kind-region/

success from Thierry-37 http://www.ctvnews.ca/world/q-a-catalonia-s-independence-push-explained-1.3624813
error404 from Thierry-37 http://tampa.cbslocal.com/2017/11/07/ranch-dressing-keg-hidden-valley/
error404 from Thierry-37 http://www.bostonherald.com/news/local_politics/2017/11/liz_warren_cashes_in_on_herald_coverage
success from Thierry-37 https://www.tvnz.co.nz/shows/the-orville
success from Thierry-37 https://www.odt.co.nz/regions/southland/three-killed-southland-crash
error404 from Thierry-37 http://www.couriermail.com.au/news/world/kim-jongun-october-10-holiday-the-latest-flash-point-that-could-lead-to-korean-war/news-story/ba6766aa4f1fd087a8e12f8f7e614c1e
success from Thierry-37 https://www.businesspost.ie/news/ireland-feel-sharia-feel-justice-feel-freedom-feel-equality-399793
success from Thierry-37 https://themoscowtimes.com/news/senators-look-to-cut-us-media-numbers-in-russia-59209
error404 from Thierry-37 https://chicago.suntimes.com/chicago-politics/writer-accuses-rev-jesse-jackson-of-sexual-harassment/
success from Thierry-37 http://www.thejakartapost.com/academia/2017/10/11/commentary-papuan-women-youth-remind-us-of-second-class-citizens.html

success from Bruno-78 http://www.npr.org/sections/thetwo-way/2017/11/05/562217575/multiple-casualties-reported-after-gunman-opens-fire-in-south-texas-church
success from Bruno-78 http://www.warsawvoice.pl/WVpage/pages/article.php/40189/news
success from Bruno-78 http://www.dw.com/fr/les-vieux-frigos-europ%C3%A9ens-v%C3%A9ritables-polluants-en-afrique/a-40850876
success from Bruno-78 http://www.independent.co.uk/news/uk/politics/labour-tories-poll-latest-lead-jeremy-corbyn-theresa-may-pm-general-election-five-points-bmg-a7988166.html
error404 from Bruno-78 http://abc13.com/road-rage-victim-tells-abc13-what-led-to-shooting/2616988/
success from Bruno-78 http://www.hindustantimes.com/india-news/india-must-stick-to-fiscal-consolidation-says-pm-modi-s-economic-advisory-council/story-lMCT8eVsJBcrVx9j3sokwN.html
success from Bruno-78 http://decoetart.over-blog.com/
success from Bruno-78 http://www.thenational.com.pg/lupari-wants-focus-services/
success from Bruno-78 https://www.seattletimes.com/seattle-news/politics/election-day-2017-live-updates-seattle-mayor-bellevue-king-county/
error404 from Bruno-78 http://detroit.cbslocal.com/2017/11/07/oreilly-auto-parts-murder-arrests-update/
success from Bruno-78 http://www.huffingtonpost.co.uk/?country=UK
success from Bruno-78 https://www.thesun.co.uk/news/4638007/trouble-for-theresa-as-labour-pull-ahead-of-tories-and-more-voters-prefer-jeremy-corbyn-as-pm/
success from Bruno-78 http://www.newsweek.com/new-york-elections-what-constitutional-convention-why-should-voters-care-703777
error404 from Bruno-78 http://news.sky.com/story/karen-bradley-insists-more-than-90-of-tory-mps-back-theresa-may-11072357
success from Bruno-78 http://en.mercopress.com/2017/10/12/obama-officials-treated-special-relationship-with-britain-as-a-joke-and-liked-to-refer-to-falklands-as-malvinas
timeoutWithContent from Bruno-78 http://www.dailymail.co.uk/tvshowbiz/article-4960002/Phillip-Schofield-enjoys-night-daughter-Ruby.html


success from Dominique-7 http://www.arabnews.com/node/1175921/middle-east
success from Dominique-7 http://www.jordantimes.com/news/region/fighters-raqqa-frontline-brace-final-showdown-daesh
error404 from Dominique-7 http://newyork.cbslocal.com/2017/11/07/roy-halladay-plane-crash/
error404 from Dominique-7 http://www.buenosairesherald.com/article/226417/explainer-maduro%E2%80%99s-constituent--assembly
success from Dominique-7 http://indianexpress.com/article/business/economic-advisory-council-identifies-10-key-areas-to-focus-on-critical-policy-interventions-4885067/
success from Dominique-7 http://www.laweekly.com/music/tokimonsta-battled-back-from-moyamoya-and-brain-surgery-to-make-the-excellent-lune-rouge-8827994
success from Dominique-7 http://www.express.co.uk/news/royal/863798/Queen-Balmoral-summer-holiday-Craithie-church-Prince-Philip-England-Prince-Charles
success from Dominique-7 http://www.deccanherald.com/content/637343/mukul-roy-quits-trinamool-rajya.html
success from Dominique-7 http://observer.com/2017/11/monday-night-football-ratings-nfl-lions-packers/
success from Dominique-7 https://wtop.com/virginia/2017/11/democrats-come-close-to-retaking-virginia-house/
success from Dominique-7 http://www.radionz.co.nz/news/world/341193/trump-ties-border-wall-to-dreamer-plan

success from Laure-20 http://www.sfchronicle.com/business/article/California-could-ban-gasoline-cars-if-12259588.php
success from Laure-20 http://www.skynews.com.au/news/top-stories/2017/10/09/nsw-government-moves-to-avoid-energy-crisis.html
error404 from Laure-20 http://boston.cbslocal.com/2017/11/07/shrewsbury-fatal-hit-and-run/
success from Laure-20 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
success from Laure-20 http://sunnewsonline.com/fish-out-assassins-of-ex-head-of-service-group-urges-lalong/
success from Laure-20 http://www.gulf-times.com/story/566982/Media-role-in-educating-people-about-dangers-of-dr

success from Morgane-94 http://montrealgazette.com/news/local-news/thanksgiving-whats-open-and-closed-on-monday
success from Morgane-94 https://www.bangkokpost.com/news/general/1340223/king-of-bhutan-to-attend-ceremony
success from Morgane-94 https://thewest.com.au/news/wa/secret-harbour-crash-victim-will-continue-to-fight-in-rph-ng-b88624008z
success from Morgane-94 http://www.breitbart.com/texas/2017/11/07/texas-church-killer-escaped-mental-hospital-2012-says-report/
success from Morgane-94 http://www.huffingtonpost.ca/2017/10/07/chrystia-freeland-gives-bleak-anti-globalization-history-book-to-nafta-partners_a_23235938/?utm_hp_ref=ca-homepage
error404 from Morgane-94 https://www.irishtimes.com/news/crime-and-law/courts/high-court/anorexic-girl-missing-ireland-terribly-during-uk-treatment-1.3249795
timeoutWithContent from Morgane-94 http://www.philly.com/philly/sports/eagles/nfl-power-rankings-tamba-hali-philadelphia-eagles-dallas-cowboys-20171107.html
success from Morgane-94 http://www.seattlepi.com/local/politics/article/Connely-Durkan-grabs-lead-for-Mayor-Mosqueda-12339465.php
success from Morgane-94 http://www.bbc.com/news/world-us-canada-41543631



89
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee/
/home/hayj/Data/Misc/error404/from-csv-list/ok/76YJAYI1SK-15109098899329667.html ==> ww.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219
/home/hayj/Data/Misc/error404/from-csv-list/ok/WDVCGP8Z1V-15109098993766768.html ==> ww.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.herald.ie/news/crime-lord-gilligans-seized-house-could-be-used-to-help-homeless-36208115.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/C2H048P6HH-15109099033338716.html ==> ww.herald.ie/news/crime-lord-gilligans-seized-house-could-be-used-to-help-homeless-36208115.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 https://www.thetimes.co.uk/edition/news/theresa-may-plots-to-demote-boris-johnson-in-reshuffle-fn36vztvd
/home/hayj/Data/Misc/error404/from-csv-list/ok/ILHVFD2668-15109099076393023.html ==> www.thetimes.co.uk/edition/news/theresa-may-plots-to-demote-boris-johnson-in-reshuffle-fn36vztvd
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.france24.com/fr/20171009-france-qatar-egypte-elections-unesco-querelles-diplomatiques-azoulay-khattab
/home/hayj/Data/Misc/error404/from-csv-list/ok/WWTB6KP091-15109099148384068.html ==> ww.france24.com/fr/20171009-france-qatar-egypte-elections-unesco-querelles-diplomatiques-azoulay-khattab
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
error404 from Élodie-81 http://dfw.cbslocal.com/2017/11/07/denton-paper-ballots/
/home/hayj/Data/Misc/error404/from-csv-list/ok/ODVIGJH67H-15109099203080103.html ==> fw.cbslocal.com/2017/11/07/denton-paper-ballots/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
error404 from Élodie-81 http://www.adelaidenow.com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f
/home/hayj/Data/Misc/error404/from-csv-list/ok/HDK0505I2H-15109099274045796.html ==> ww.adelaidenow.com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/G50C5LUL70-15109099317937365.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 https://www.standardmedia.co.ke/article/2001256918/one-shot-two-run-over-by-motorist-as-anti-iebc-protests-turn-violent
/home/hayj/Data/Misc/error404/from-csv-list/ok/2BJLYO5S48-1510909937475405.html ==> www.standardmedia.co.ke/article/2001256918/one-shot-two-run-over-by-motorist-as-anti-iebc-protests-turn-violent
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
error404 from Élodie-81 http://washington.cbslocal.com/2017/11/06/caps-overcome-2-goal-deficit-win-in-ot/
/home/hayj/Data/Misc/error404/from-csv-list/ok/HGARKTBJPI-15109099433019402.html ==> ashington.cbslocal.com/2017/11/06/caps-overcome-2-goal-deficit-win-in-ot/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
/home/hayj/Data/Misc/error404/from-csv-list/ok/EMXOI429H1-1510909950229114.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
error404 from Élodie-81 http://minnesota.cbslocal.com/2017/11/07/target-closings/
/home/hayj/Data/Misc/error404/from-csv-list/ok/3JLVLE67VA-15109099542624152.html ==> innesota.cbslocal.com/2017/11/07/target-closings/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/KPI1E1KECQ-15109099642536047.html ==> ww.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 https://timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms
/home/hayj/Data/Misc/error404/from-csv-list/ok/DXB5OQVI3O-15109099722291846.html ==> timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.caribbeannews.com/
/home/hayj/Data/Misc/error404/from-csv-list/ok/PLD62PIXEX-15109099813891938.html ==> ww.caribbeannews.com/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
success from Élodie-81 http://www.huffingtonpost.fr/2017/10/08/seminaire-gouvernemental-pourquoi-edouard-philippe-reunit-son-equipe-a-matignon-ce-dimanche_a_23236296/?utm_hp_ref=fr-homepage
/home/hayj/Data/Misc/error404/from-csv-list/ok/5YXPZ6S34H-1510909986691676.html ==> ww.huffingtonpost.fr/2017/10/08/seminaire-gouvernemental-pourquoi-edouard-philippe-reunit-son-equipe-a-matignon-ce-dimanche_a_23236296/?utm_hp_ref=fr-homepage
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
error404 from Élodie-81 http://www.pravdareport.com/news/world/americas/09-10-2017/138865-unmanned_orca_submarine-0/
/home/hayj/Data/Misc/error404/from-csv-list/ok/6U182Z8Z9D-1510909995399957.html ==> ww.pravdareport.com/news/world/americas/09-10-2017/138865-unmanned_orca_submarine-0/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE







106
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Anne-marie-94 http://gothamist.com/2017/11/02/west_side_bike_path_security.php
/home/hayj/Data/Misc/error404/from-csv-list/ok/DHRYGEI9ST-15109101057354321.html ==> othamist.com/2017/11/02/west_side_bike_path_security.php
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 https://www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks
/home/hayj/Data/Misc/error404/from-csv-list/ok/JVXSR8YRUQ-15109101157371018.html ==> www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 https://www.washingtontimes.com/news/2017/nov/7/schumer-predicts-dreamer-amnesty-will-be-part-year/
/home/hayj/Data/Misc/error404/from-csv-list/ok/XWRFQCVF6J-15109101205707128.html ==> www.washingtontimes.com/news/2017/nov/7/schumer-predicts-dreamer-amnesty-will-be-part-year/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Anne-marie-94 http://chicago.cbslocal.com/2017/11/07/felony-franks-closed/
/home/hayj/Data/Misc/error404/from-csv-list/ok/9GHDL47I3S-15109101266190445.html ==> hicago.cbslocal.com/2017/11/07/felony-franks-closed/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 http://www.deccanchronicle.com/nation/current-affairs/111017/solar-scam-pinarayi-vijayan-orders-vigilance-probe-against-oommen-chandy.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/D36B4I5LRA-15109101339333255.html ==> ww.deccanchronicle.com/nation/current-affairs/111017/solar-scam-pinarayi-vijayan-orders-vigilance-probe-against-oommen-chandy.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 http://punchng.com/new-york-police-reopens-2004-weinstein-assault-case/
/home/hayj/Data/Misc/error404/from-csv-list/ok/AZUENPT7RP-15109101378306146.html ==> unchng.com/new-york-police-reopens-2004-weinstein-assault-case/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/5I0SJ94XKW-1510910146727734.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 http://www.ansa.it/english/news/2017/10/09/battisti-toasts-freedom-after-release-in-brazil_71cd224c-5156-41c4-a6eb-c89e8833d41f.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/BXJ4ZGECCP-15109101502550595.html ==> ww.ansa.it/english/news/2017/10/09/battisti-toasts-freedom-after-release-in-brazil_71cd224c-5156-41c4-a6eb-c89e8833d41f.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 http://nation.com.pk/national/11-Oct-2017/iranian-envoy-lauds-pakistan-s-efforts-for-regional-stability
/home/hayj/Data/Misc/error404/from-csv-list/ok/LGGTOX2MHT-15109101530817149.html ==> ation.com.pk/national/11-Oct-2017/iranian-envoy-lauds-pakistan-s-efforts-for-regional-stability
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Anne-marie-94 https://beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833/
/home/hayj/Data/Misc/error404/from-csv-list/ok/FFSBTUL4KF-15109101600287077.html ==> beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 http://riotimesonline.com/brazil-news/rio-politics/armed-forces-return-in-search-operation-of-rios-rocinha-favela/
/home/hayj/Data/Misc/error404/from-csv-list/ok/582856CB6C-15109101657913878.html ==> iotimesonline.com/brazil-news/rio-politics/armed-forces-return-in-search-operation-of-rios-rocinha-favela/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anne-marie-94 https://www.businesslive.co.za/bd/companies/2017-10-12-reserve-bank-probing-bank-of-baroda-after-outa-allegations/
/home/hayj/Data/Misc/error404/from-csv-list/ok/RVMTKF2V57-15109101707642014.html ==> www.businesslive.co.za/bd/companies/2017-10-12-reserve-bank-probing-bank-of-baroda-after-outa-allegations/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Anne-marie-94 http://www.heraldsun.com.au/lifestyle/health/body-soul-daily/not-sleeping-best-insomnia-cure-could-be-ignoring-it/news-story/0734f87ce37af05d024619d4d9beaff5
/home/hayj/Data/Misc/error404/from-csv-list/ok/6OMYP9DP7V-15109101796517143.html ==> ww.heraldsun.com.au/lifestyle/health/body-soul-daily/not-sleeping-best-insomnia-cure-could-be-ignoring-it/news-story/0734f87ce37af05d024619d4d9beaff5
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE




119
/home/hayj/Data/Misc/error404/from-csv-list/ok/IQ8574H6T0-15109107986939414.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/RCZCI88JUS-1510910802732392.html ==> ww.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole
/home/hayj/Data/Misc/error404/from-csv-list/ok/U2AH0DKDBA-1510910812195451.html ==> algaryherald.com/sports/hockey/nhl/calgary-flames/flames-enter-haunted-honda-center-hoping-to-break-curse
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://calgaryherald.com/sports/hockey/nhl/calgary-flames/flames-enter-haunted-honda-center-hoping-to-break-curse
/home/hayj/Data/Misc/error404/from-csv-list/ok/0JQBW2WJT5-15109108213214712.html ==> ww.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12
/home/hayj/Data/Misc/error404/from-csv-list/ok/VC0LXX01Y8-15109108312553406.html ==> tla.com/2017/11/08/trump-arrives-in-beijing-for-high-stakes-visit-with-chinese-president/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 http://ktla.com/2017/11/08/trump-arrives-in-beijing-for-high-stakes-visit-with-chinese-president/
/home/hayj/Data/Misc/error404/from-csv-list/ok/EWJCCYKSDP-15109108373325193.html ==> local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 https://local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653
/home/hayj/Data/Misc/error404/from-csv-list/ok/NNDOF78Q2W-15109108420394354.html ==> ww.nation.co.ke/news/Nasa-protests-in-Nairobi-city-centre-Fred-Matiangi/1056-4136704-7tc9a1z/index.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.nation.co.ke/news/Nasa-protests-in-Nairobi-city-centre-Fred-Matiangi/1056-4136704-7tc9a1z/index.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/GJATKGKMBJ-15109108507407775.html ==> www.vanguardngr.com/2017/10/senate-begins-consideration-buharis-5-5bn-loan/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 https://www.vanguardngr.com/2017/10/senate-begins-consideration-buharis-5-5bn-loan/
/home/hayj/Data/Misc/error404/from-csv-list/ok/OXCOUEUV3A-15109108655998743.html ==> ww.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272
/home/hayj/Data/Misc/error404/from-csv-list/ok/H0WVBCEADX-15109108713375962.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
timeoutWithContent from Gérard-28 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/C4BQZYNEXJ-15109108976432495.html ==> www.usatoday.com/story/news/politics/2017/10/08/trump-blasts-sen-bob-corker-negative-voice-gop-agenda/744071001/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
/home/hayj/Data/Misc/error404/from-csv-list/ok/F30S2HKMBG-15109109258873062.html ==> ww.egyptindependent.com/valuable-wild-salmon-fishery-world-trump-administration-become-mine/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
timeoutWithContent from Gérard-28 http://www.egyptindependent.com/valuable-wild-salmon-fishery-world-trump-administration-become-mine/
/home/hayj/Data/Misc/error404/from-csv-list/ok/FZ844VWQKO-1510910952390783.html ==> ancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
timeoutWithContent from Gérard-28 http://vancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3
/home/hayj/Data/Misc/error404/from-csv-list/ok/WU0N91S5VN-15109109782598839.html ==> ietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
timeoutWithContent from Gérard-28 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
/home/hayj/Data/Misc/error404/from-csv-list/ok/ZUGC2YSC3H-15109110051843581.html ==> ww.latimes.com/entertainment/movies/la-et-mn-harvey-weinstein-rise-fall-20171008-story.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
timeoutWithContent from Gérard-28 http://www.latimes.com/entertainment/movies/la-et-mn-harvey-weinstein-rise-fall-20171008-story.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/CHJFS2E181-15109110309816453.html ==> osangeles.cbslocal.com/2017/11/07/morey-boogie-board-inventor/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 http://losangeles.cbslocal.com/2017/11/07/morey-boogie-board-inventor/
/home/hayj/Data/Misc/error404/from-csv-list/ok/NAPBCKDOPO-15109110373300586.html ==> www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp
/home/hayj/Data/Misc/error404/from-csv-list/ok/T1LT28WFOX-15109110420776289.html ==> ww.reuters.com/article/us-texas-shooting/texas-gunmans-in-laws-sometimes-attended-church-sheriff-says-idUSKBN1D510F?feedType=RSS&feedName=domesticNews
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.reuters.com/article/us-texas-shooting/texas-gunmans-in-laws-sometimes-attended-church-sheriff-says-idUSKBN1D510F?feedType=RSS&feedName=domesticNews
/home/hayj/Data/Misc/error404/from-csv-list/ok/JR2QTCIYSA-15109110500495732.html ==> ww.mercurynews.com/2017/11/07/brainstorming-the-bay-area-housing-crisis-thousands-sign-up-for-community-wide-conversation/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.mercurynews.com/2017/11/07/brainstorming-the-bay-area-housing-crisis-thousands-sign-up-for-community-wide-conversation/
/home/hayj/Data/Misc/error404/from-csv-list/ok/VQ3BPRII3I-15109110562501106.html ==> ww.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 http://www.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years/
/home/hayj/Data/Misc/error404/from-csv-list/ok/AB487L4CCF-15109110623084092.html ==> amaica-gleaner.com/article/lead-stories/20171012/transport-authority-spends-millions-secure-rat-infested-building
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 http://jamaica-gleaner.com/article/lead-stories/20171012/transport-authority-spends-millions-secure-rat-infested-building
/home/hayj/Data/Misc/error404/from-csv-list/ok/A2HTYVUBNA-15109110687857237.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
/home/hayj/Data/Misc/error404/from-csv-list/ok/YT1A5S7RO6-1510911076926738.html ==> ww.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/4FMDWUMVXL-15109110898822365.html ==> ww.palestinechronicle.com/the-balfour-declaration-destroyed-palestine-not-the-palestinian-people/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.palestinechronicle.com/the-balfour-declaration-destroyed-palestine-not-the-palestinian-people/
/home/hayj/Data/Misc/error404/from-csv-list/ok/MERZDVWRMJ-1510911093825521.html ==> mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Gérard-28 https://mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications
/home/hayj/Data/Misc/error404/from-csv-list/ok/8YSD969FTQ-15109110994526384.html ==> ww.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage
/home/hayj/Data/Misc/error404/from-csv-list/ok/Q1B39YR255-1510911106988811.html ==> ww.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini
/home/hayj/Data/Misc/error404/from-csv-list/ok/M39YJ0XZPX-15109111086850789.html ==> www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
/home/hayj/Data/Misc/error404/from-csv-list/ok/JBDDZFAL1B-15109111099576373.html ==> ww.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658/
/home/hayj/Data/Misc/error404/from-csv-list/ok/GE2J41DDV6-15109111184025404.html ==> ww.jamaicaobserver.com/news/senators-bid-farewell-to-golding-brown-burke_113570
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Gérard-28 http://www.jamaicaobserver.com/news/senators-bid-farewell-to-golding-brown-burke_113570
/home/hayj/Data/Misc/error404/from-csv-list/ok/7PJR8RNID1-15109111253565397.html ==> bcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...




/home/hayj/Data/Misc/error404/from-csv-list/ok/DVJQ6K2OYM-15109113394449344.html ==> www.kyivpost.com/ukraine-politics-2/lutsenko-says-russian-fsb-involved-kyiv-assassination-former-duma-lawmaker.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 https://www.kyivpost.com/ukraine-politics-2/lutsenko-says-russian-fsb-involved-kyiv-assassination-former-duma-lawmaker.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/UNIJMXNNNB-1510911349301795.html ==> ww.itn.co.uk/press-releases/itn-productions-appoints-head-of-news/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.itn.co.uk/press-releases/itn-productions-appoints-head-of-news/
/home/hayj/Data/Misc/error404/from-csv-list/ok/JUNPG1Y2WA-15109113525474079.html ==> ww.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp
/home/hayj/Data/Misc/error404/from-csv-list/ok/RJN27DLLZN-1510911360839569.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/45LD40P32G-15109113655855908.html ==> ww.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450
/home/hayj/Data/Misc/error404/from-csv-list/ok/NTDCR2ANSX-15109113705297718.html ==> exiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://mexiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage/
/home/hayj/Data/Misc/error404/from-csv-list/ok/PAZRS33SZY-15109113751219828.html ==> www.usatoday.com/story/news/politics/2017/10/08/trump-blasts-sen-bob-corker-negative-voice-gop-agenda/744071001/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 https://www.usatoday.com/story/news/politics/2017/10/08/trump-blasts-sen-bob-corker-negative-voice-gop-agenda/744071001/
/home/hayj/Data/Misc/error404/from-csv-list/ok/WVJLCUF4Z0-15109113811961238.html ==> ww.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/9A9NFBMY0R-15109113848765662.html ==> www.stuff.co.nz/business/small-business/97687085/wellington-restaurant-closes-after-selling-two-illegal-wines-and-a-beer
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 https://www.stuff.co.nz/business/small-business/97687085/wellington-restaurant-closes-after-selling-two-illegal-wines-and-a-beer
/home/hayj/Data/Misc/error404/from-csv-list/ok/K6UKSGEO63-1510911393368692.html ==> ww.foxnews.com/us/2017/10/08/vice-president-mike-pence-leaves-colts-49ers-game-after-players-reportedly-kneel.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 http://www.foxnews.com/us/2017/10/08/vice-president-mike-pence-leaves-colts-49ers-game-after-players-reportedly-kneel.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/S329M0CADG-15109114051105564.html ==> elpais.com/elpais/2017/10/09/inenglish/1507534094_516802.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Raphaël-26 https://elpais.com/elpais/2017/10/09/inenglish/1507534094_516802.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/HCN4WNQDIR-15109114115045254.html ==> ypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...


/home/hayj/Data/Misc/error404/from-csv-list/ok/KB6XGK2811-15109118951612408.html ==> www.nbcnewyork.com/news/local/Tammie-McCormick-Missing-New-York-Teenager-Cold-Case-456117483.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Anthony-14 https://www.nbcnewyork.com/news/local/Tammie-McCormick-Missing-New-York-Teenager-Cold-Case-456117483.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/2WEULOXQOT-15109119013814468.html ==> ypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...





/home/hayj/Data/Misc/error404/from-csv-list/ok/V2FVZBCRI5-15109119882665677.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
/home/hayj/Data/Misc/error404/from-csv-list/ok/6TYO3WV444-1510911994149938.html ==> ww.manilatimes.net/comelec-chief-bautista-impeached/355884/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 http://www.manilatimes.net/comelec-chief-bautista-impeached/355884/
/home/hayj/Data/Misc/error404/from-csv-list/ok/E9VBZGTLDA-15109120046979997.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/ZIGLDCVID3-1510912011426901.html ==> ww.cubanews.acn.cu/cuba/7376-eusebio-leal-calls-to-preserve-unity-of-the-nation
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
error404 from Amelie-92 http://www.cubanews.acn.cu/cuba/7376-eusebio-leal-calls-to-preserve-unity-of-the-nation
/home/hayj/Data/Misc/error404/from-csv-list/ok/VU17GPPLJV-15109120211658227.html ==> ietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
/home/hayj/Data/Misc/error404/from-csv-list/ok/F3VHSY9FKV-1510912041284539.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/9O85GGYYYH-15109120455688982.html ==> korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Amelie-92 https://korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html
/home/hayj/Data/Misc/error404/from-csv-list/ok/V0OVVH3RB0-15109120499674196.html ==> bcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...


/home/hayj/Data/Misc/error404/from-csv-list/ok/V2S7GLX8GM-1510912154089313.html ==> www.theguardian.com/world/2017/oct/08/catalonia-spain-prime-minister-refuses-rule-out-suspending-autonomy
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Guy-98 https://www.theguardian.com/world/2017/oct/08/catalonia-spain-prime-minister-refuses-rule-out-suspending-autonomy
/home/hayj/Data/Misc/error404/from-csv-list/ok/D4ZF2U3JEK-15109121569218352.html ==> ww.denverpost.com/2017/10/08/bob-corker-donald-trump-adult-day-care/
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Guy-98 http://www.denverpost.com/2017/10/08/bob-corker-donald-trump-adult-day-care/
/home/hayj/Data/Misc/error404/from-csv-list/ok/RMLTF4RJY0-15109121635040705.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Guy-98 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/70DSYWBSYG-15109121675236955.html ==> www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
refused from Guy-98 https://www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796
/home/hayj/Data/Misc/error404/from-csv-list/ok/0WDBTUFQA9-15109121694033113.html ==> bcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...




/home/hayj/Data/Misc/error404/from-csv-list/ok/KIFFNVZCFN-15109122331376843.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Lucas-9 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/AM2OKU3MK7-1510912239040493.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Lucas-9 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/PLVSKWU2FS-15109122441341991.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Lucas-9 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/ZR9ZBSVCKG-15109122540976973.html ==> bcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()



/home/hayj/Data/Misc/error404/from-csv-list/ok/SWQJH3UU0M-15109123194784176.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Monique-57 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/UTGAEMKWAP-15109123226666293.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Monique-57 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/G1FSJ850MY-15109123294008005.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Monique-57 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/Y0OV7DSXAO-15109123406929502.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Monique-57 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
/home/hayj/Data/Misc/error404/from-csv-list/ok/7WHOET352C-1510912347392279.html ==> ietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
------------Trying to exec self.stopLoading()
------------self.stopLoading() DONE
------------Trying to exec self.loadBlank()
------------self.loadBlank() DONE
Get starting...
Get DONE
success from Monique-57 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97





/home/hayj/Data/Misc/error404/from-csv-list/ok/SKD1G042R3-15109350812351665.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
Get starting...
Get DONE
success from Christine-71 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/41L3GOZCQX-15109350895800765.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
Get starting...
Get DONE
success from Christine-71 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/W9W7GM48XG-15109350977087278.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
Get starting...
Get DONE
success from Christine-71 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/6T2ID6T8V2-15109351043605838.html ==> ietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
Get starting...
timeoutWithContent from Christine-71 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
/home/hayj/Data/Misc/error404/from-csv-list/ok/7UKJ0E9QHO-15109351307125118.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
Get starting...
Get DONE
success from Christine-71 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead



/home/hayj/Data/Misc/error404/from-csv-list/ok/BBG7WEGLF0-15109352000676029.html ==> ww.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
Get starting...
Get DONE
success from Claire-4 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
/home/hayj/Data/Misc/error404/from-csv-list/ok/KIXUSGZCKV-15109352066496325.html ==> ww.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
Get starting...
Get DONE
success from Claire-4 http://www.independent.ie/videos/have-you-seen/watch-ghost-caught-on-camera-corks-oldest-school-releases-eerie-cctv-footage-36196792.html#play
/home/hayj/Data/Misc/error404/from-csv-list/ok/1AZ30WVSNZ-15109352145712893.html ==> ietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
Get starting...
Get DONE
success from Claire-4 http://vietnamnews.vn/politics-laws/405390/australian-embassy-launches-logo-contest-to-celebrate-vn-diplomatic-relations.html#KVSuPDjt1bCgOHie.97
/home/hayj/Data/Misc/error404/from-csv-list/ok/7SM5FW2R14-15109352302817109.html ==> www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
Get starting...
Get DONE
success from Claire-4 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
/home/hayj/Data/Misc/error404/from-csv-list/ok/D84415Y16L-151093523701151.html ==> ww.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
Get starting...
Get DONE
success from Claire-4 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead




""")


old = """



https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 https://www.telegraphindia.com/1171011/jsp/frontpage/story_177698.jsp
http://www.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.chron.com/sports/astros/article/Astros-Carlos-Correa-hangs-out-fans-Burger-Joint-12258293.php?ipid=hpctp
http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.stltoday.com/news/local/crime-and-courts/election-day-st-louis-voters-today-decide-fate-of-sales/article_5816507b-a632-54f3-bb7a-00ebe6adab8a.html#tracking-source%3Dhome-featured
http://dfw.cbslocal.com/2017/11/07/denton-paper-ballots/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 http://dfw.cbslocal.com/2017/11/07/denton-paper-ballots/
https://timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 https://timesofindia.indiatimes.com/adv-7-reasons-why-the-asus-zenfone-4-selfie-series-is-the-real-selfie-expert/articleshow/61019640.cms
http://www.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.huffingtonpost.com.au/2017/10/08/backpacker-victims-of-violent-salt-creek-attack-share-harrowing-story_a_23236445/?utm_hp_ref=au-homepage
http://www.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.smh.com.au/comment/deadly-flu-season-should-mean-vaccines-for-all-health-workers-20171008-gywgz6.html
http://www.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.denverpost.com/2017/11/07/colorado-springs-woman-jailed-pretrial-fee/
http://www.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.theaustralian.com.au/life/travel/travel-bucket-list-unesco-sites-to-behold/news-story/b8efb616fe6a69d143428de695068d12
http://chicago.cbslocal.com/2017/11/07/felony-franks-closed/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 http://chicago.cbslocal.com/2017/11/07/felony-franks-closed/
http://www.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
timeoutWithContent from Chloe-0 http://www.telegraph.co.uk/music/artists/life-strictly-reverend-richard-coless-drug-fuelled-disco-years/
https://www.kyivpost.com/ukraine-politics-2/lutsenko-says-russian-fsb-involved-kyiv-assassination-former-duma-lawmaker.html
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
http://www.itn.co.uk/press-releases/itn-productions-appoints-head-of-news/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.itn.co.uk/press-releases/itn-productions-appoints-head-of-news/
http://www.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
timeoutWithContent from Chloe-0 http://www.newsmax.com/Headline/texas-church-shooting-mental-hospital/2017/11/07/id/824658/
http://www.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
timeoutWithContent from Chloe-0 http://www.aljazeera.com/news/2017/10/spain-takes-step-suspending-catalonia-autonomy-171011104701935.html
https://www.nbcnews.com/news/world/north-korea-s-kim-jong-praises-his-nuclear-weapons-powerful-n808796
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
http://www.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
timeoutWithContent from Chloe-0 http://www.theage.com.au/national/health/how-the-flu-kills-what-happens-when-a-person-dies-with-influenza-20171005-gyv9r1.html
https://korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 https://korben.info/bluefiles-securisez-lenvoi-de-vos-donnees-confidentielles.html
http://gothamist.com/2017/11/02/west_side_bike_path_security.php
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 http://gothamist.com/2017/11/02/west_side_bike_path_security.php
http://www.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.jpost.com/International/Jews-condemn-anti-Muslim-London-mosque-backlash-507219
http://www.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.solomonstarnews.com/index.php/news/business/item/19495-express-freight-now-cargo-agent-for-air-niugini
http://vancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
timeoutWithContent from Chloe-0 http://vancouversun.com/pmn/news-pmn/canada-news-pmn/b-c-attorney-general-says-serious-lack-of-sheriffs-involves-low-pay/wcm/71e603b3-51b9-4322-bc6d-7011a433f8b3
http://www.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.torontosun.com/2017/10/07/ex-deputy-education-minister-jailed-for-child-porn-charges-out-on-parole
http://www.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.cbc.ca/news/canada/montreal/fatal-fire-quebec-cap-chat-mother-twin-daughters-1.4346450
http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.miamiherald.com/news/local/community/miami-dade/coral-gables/article183249036.html#navlink%3DLead
https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 https://www.japantimes.co.jp/news/2017/10/11/business/scandals-seen-shredding-japan-inc-s-revered-image-quality/#.Wd4flWi0PIU
https://local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 https://local.theonion.com/weak-willed-coward-changes-opinion-after-learning-he-wa-1820220653
https://beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 https://beta.theglobeandmail.com/news/world/us-politics/trump-administration-cites-edmonton-attack-in-call-for-immigration-changes/article36524833/
https://www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 https://www.channel4.com/news/councils-denied-cash-for-sprinklers-in-tower-blocks
http://www.caribbeannews.com/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.caribbeannews.com/
http://www.adelaidenow.com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 http://www.adelaidenow.com.au/business/statewide-super-has-unveiled-a-150000-sponsorship-program-to-help-boost-womens-sports-in-south-australia/news-story/761070c2d24018668895d180f633b08f
http://mexiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage/
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://mexiconewsdaily.com/news/13-buildings-on-list-in-demolitions-first-stage/
http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
success from Chloe-0 http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11931272
https://mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE
error404 from Chloe-0 https://mg.co.za/article/2017-10-11-uct-professor-mamokgethi-phakeng-and-accusations-of-fake-qualifications
http://calgaryherald.com/sports/hockey/nhl/calgary-flames/flames-enter-haunted-honda-center-hoping-to-break-curse
Trying to exec self.stopLoading()
self.stopLoading() DONE
Trying to exec self.loadBlank()
self.loadBlank() DONE



"""


exclude = urlParser.strToUrls("""
https://www.yahoo.com/news/
https://fr.news.yahoo.com/
https://news.google.com/news/
https://news.google.fr/
http://decoetart.over-blog.com/
""")


if __name__ == '__main__':
    pass





