import urllib, os
import json as m_json
import string

sites = [
'042-young-teen-masturbates-using-a-dildo/',
'043-nice-chick-finger-fucks-her-pussy/',
'044-redhead-babe-strips-on-cam/',
'045-dildoing-under-the-sheets/',
'046-horny-babe-films-self-while-fingering-her-pussy/',
'047-busty-chick-fucks-her-cunt-with-a-dildo/',
'048-hot-redhead-striptease/',
'049-amazing-pussy-lips-stretch/',
'050-hot-slim-chicks-striptease/',
'051-horny-babe-strips-while-filming-herself/',
'052-young-teen-chick-does-a-naughty-striptease/',
'053-hot-kinky-babe-films-herself/',
'054-chick-strips-top-and-films-self/',
'055-topless-teen-does-sexy-dance/',
'056-naked-chick-in-the-shower/',
'057-horny-teen-does-a-striptease/',
'058-topless-teen-films-self-while-dancing/',
'059-sexy-chicks-naughty-striptease/',
'060-blonde-hottie-flashes-tits-while-dancing/',
'074-hot-pole-dancer-with-nice-pair-of-titties/',
'075-chick-displays-her-amazing-set-of-racks/',
'076-busty-teen-strips-while-dancing/',
'077-lovely-chick-being-a-tease-on-cam/',
'078-this-bitch-is-such-a-tease/',
'079-nice-naked-chick-fingering-her-pussy/',
'080-webcam-hottie-masturbates-for-a-chatmate/',
'081-pretty-gf-plays-with-self-on-the-floor/',
'082-topless-blonde-masturbates-on-bed/',
'083-hottie-squeezes-tits-while-dancing/',
'084-webcam-hottie-shows-her-perky-tits/',
'085-lovely-amateur-babe-goes-topless/',
'086-amateur-webcam-tease-goes-topless/',
'087-pretty-girls-sexy-striptease/',
'088-webcam-hottie-strips-and-masturbates/',
'089-gorgeous-babe-displays-her-shaven-twat/',
'090-hot-teen-with-perfect-tits-and-ass/',
'091-sexy-blonde-shows-her-firm-breasts/',
'092-pretty-amateur-chick-playing-with-herself/',
'093-hottie-in-sexy-maid-outfit-masturbating/',
'094-amateur-bitch-does-kinky-pole-dancing/',
'096-webcam-babe-films-self-while-strip-dancing/',
'097-hot-babes-sexy-dance-inside-her-bedroom/',
'098-amateur-babe-with-nice-boobs/',
'099-naked-chicks-got-an-awesome-ass/',
'100-sexy-blonde-teen-dancing-in-her-room/',
'101-naked-chick-films-self-while-masturbating/',
'102-big-tittied-cutie-strips-on-the-webcam/',
'103-sexy-chick-pole-dancing-in-her-room/',
'104-gorgeous-babe-with-nice-titties/',
'105-horny-chick-masturbates-on-her-bed/',
'106-chick-with-perky-tits-masturbates-on-sink/',
'107-amateur-teens-sexy-stripdance-in-her-bedroom/',
'108-naked-cutie-touching-herself-in-a-bath-tub/',
'109-amateur-blonde-fucks-a-bed-post/',
'110-busty-chick-strips-off-clothes-in-her-room/',
'111-naked-cutie-masturbating-on-her-bed/',
'112-topless-hottie-shows-tits-on-webcam/',
'113-webcam-cutie-naked-on-her-bed/',
'114-masturbating-babe-tastes-her-own-cum/',
'115-playing-with-her-twat-while-in-the-tub/',
'116-blonde-cutie-doing-a-sexy-striptease/',
'117-emo-babe-fingering-her-pussy/',
'118-naked-hottie-plays-with-self-on-cam/',
'119-horny-teen-fingering-her-cunt/',
'120-stripdancing-babe-in-skimpy-bikini/',
'121-sexy-blonde-fingering-on-chair/',
'122-amateur-bombshells-hot-striptease/',
'123-sexy-hottie-naked-in-the-bath/',
'124-naked-chick-rubbing-her-pussy/',
'125-blonde-cutie-films-her-striptease/',
'126-pretty-gf-goes-topless/',
'127-horny-teen-gets-naked-on-webcam/',
'128-horny-girl-masturbates-on-tub/',
'129-busty-hottie-gets-naked-for-chatmate/',
'130-masturbating-and-playing-on-cam/',
'131-chick-plays-with-her-perky-titties/',
'132-webcam-gf-flashes-nice-tits-and-ass/',
'133-gorgeous-asian-babe-strips-on-cam/',
'134-mitch-gets-naughty-with-chatmate/',
'135-sexy-chick-in-black-lingerie/',
'136-horny-teen-masturbates-on-the-floor/',
'137-fucking-herself-with-a-vibrator/',
'138-hottie-with-a-perfect-round-ass/',
'139-naked-cutie-fingers-her-cunt/',
'140-busty-teen-teasing-a-chatmate/',
'141-latina-bombshell-naked-on-cam/',
'142-cutie-masturbates-after-a-striptease/',
'143-amateur-teen-displays-tits-on-cam/',
'144-sexy-chick-strips-naked-on-a-chair/',
'145-blonde-amateur-girls-nip-slip/',
'146-busty-girl-films-self-naked/',
'147-horny-jane-cums-while-fingering/',
'148-amateur-cutie-gets-naked/',
'149-webcam-bombshell-flashes-her-tits/',
'150-hot-chick-strips-on-cam/',
'151-amateur-teens-striptease-in-her-room/',
'152-busty-webcam-bitch-goes-topless/',
'153-pretty-babe-displays-her-boobies/',
'154-naked-teen-masturbates-on-a-chair/',
'155-webcam-girlfriend-showing-her-tits/',
'156-naked-busty-cutie-teasing-her-bf/',
'157-wild-teen-shakes-her-booty/',
'158-amateur-babe-gets-naughty-with-cam/',
'159-asian-cutie-gets-kinky-on-webcam/',
'160-amateur-bombshells-hot-striptease/',
'161-naughty-webcam-scene-chick/',
'162-shy-bitch-flashes-tits-on-webcam/',
'163-sexy-girl-with-perky-breasts/',
'164-pam-displays-her-nice-ass-and-tits/',
'165-cutie-chick-plays-with-her-cunt/',
'166-fucking-herself-with-a-lava-lamp/',
'167-pretty-bitch-gets-naked-on-cam/',
'168-amateur-teen-with-nice-ass/',
'169-hot-gf-films-herself-naked/',
'170-busty-cutie-in-a-sexy-stripdance/',
'171-gf-masturbates-on-hidden-cam/',
'172-poking-her-tight-pussy/',
'173-amateur-webcam-bombshell/',
'174-naked-cutie-in-the-showers/',
'175-hottie-gets-naked-on-cam/',
'176-busty-webcam-amateur-cutie/',
'177-hot-gfs-cam-striptease/',
'178-mindy-playing-with-her-breasts/',
'179-naked-heavy-chested-girlfriend/',
'180-amateur-cutie-masturbating/',
'181-hottie-plays-with-herself/',
'182-stuffing-her-cunt-with-a-hairbrush/',
'183-sexy-naked-chick-in-the-showers/',
'184-rubbing-and-fingering-her-pussy/',
'185-horny-amateur-webcam-gf/',
'186-hot-babes-kinky-striptease/',
'187-horny-in-front-of-the-mirror/',
'188-big-tittied-webcam-bitch/',
'189-wild-bikini-slut-on-a-bed/',
'190-busty-cutie-plays-with-her-cunt/',
'191-webcam-hottie-sucks-on-a-dildo/',
'192-slutty-chick-in-her-skimpy-bikini/',
'193-busty-hottie-films-self-on-the-bed/',
'194-babe-in-bathrobe-displays-her-tits/',
'195-sizzling-hot-girlfriends-striptease/',
'196-naked-asian-chick-humps-a-pillow/',
'197-blindfolded-hottie-masturbating/',
'198-blonde-cutie-pokes-her-twat/',
'199-babe-in-thongs-flashes-tits/',
'200-hot-amateur-striptease/',
'201-voyeur-watches-gf-strip/',
'202-naked-teen-plays-with-her-pussy/',
'203-topless-lara-teasing-her-chatmate/',
'204-naked-chick-plays-with-popsicle/',
'205-showing-off-her-nice-breasts/',
'206-bombshell-in-double-penetration/',
'207-sexy-sams-hot-kinky-video/',
'208-webcam-teen-in-her-green-bra/',
'209-hot-tamara-flashing-her-butt-cheeks/',
'210-sexy-teen-tries-on-various-lingerie/',
'211-hot-babe-strips-off-on-cam/',
'212-sexy-asian-girl-gets-naughty/',
'213-raunchy-bitch-flashes-nice-tits/',
'214-naughty-cutie-gets-naked-and-plays/',
'215-webcam-babe-shows-off-her-breasts/',
'216-hardcore-chick-fingers-her-pussy/',
'217-busty-hottie-with-nice-tits-and-ass/',
'218-babe-spreads-and-masturbates/',
'219-horny-cutie-plays-in-the-nude/',
'220-hot-and-sexy-teens-striptease/',
'222-sexy-cuties-striptease-in-her-room/',
'223-teasing-her-chatmates-in-the-showers/',
'224-amateur-gf-in-a-kinky-dance/'];






sites2 = [
'223-horny-chick-masturbates-with-brush/',
'224-hot-pussy-and-blowjob/',
'225-horny-chick-squirts-loads/',
'226-hot-blowjob-in-cable-car/',
'227-banging-in-the-morning/',
'228-horny-sluts-masturbate-together/',
'229-girlfriend-shaves-and-masturbates/',
'230-girlfriend-films-herself-while-masturbating/',
'231-girlfriend-rides-her-boyfriends-cock-hard/',
'232-night-vision-cam-captures-twat-getting-fucked-deep/',
'233-sexy-gf-rubs-her-pussy/',
'234-hot-girlfriend-squirts-loads-while-masturbating/',
'235-chick-rides-bfs-cock-fast-and-hard/',
'236-horny-teen-shows-pussy-on-webcam/',
'237-dick-teasing-gfs-clit/',
'239-girlfriends-stuffed-fuck-holes/',
'240-watch-my-gf-masturbate/',
'241-chicks-pussy-got-licked-real-good/',
'242-fucking-the-gf-doggystyle/',
'243-naughty-girl-dildoing-her-pussy/',
'244-girl-cums-while-fingering-her-cunt/',
'245-horny-gf-gets-pounded-hard-from-behind/',
'246-hardcore-fucking-in-the-bedroom/',
'247-girlfriend-gets-naughty-with-bf-in-the-woods/',
'248-horny-dude-fucks-his-gf-from-behind/',
'249-hot-asian-girl-gets-fucked-hard/',
'250-watch-her-dildo-her-pussy/',
'251-she-loves-to-play-with-herself-on-cam/',
'252-horny-girl-riding-her-bestfriends-cock/',
'253-a-neighbor-toys-with-her-cunt-outdoors/',
'254-tanned-chick-touching-herself/',
'255-kinky-lesbians-in-the-dressing-room/',
'256-fucking-my-bitch-from-behind/',
'257-hardcore-fucking-in-the-kitchen/',
'258-i-almost-ripped-her-ass-open/',
'259-watch-this-blindfolded-bitch-lick-my-balls/',
'260-wild-and-sexy-dance-leads-to-hot-blowjob/',
'261-slim-girl-strips-off-bikini-and-flashes-her-tits/',
'262-naked-teen-goes-wild-in-her-bedroom/',
'263-amateur-teen-likes-dildoing-her-pussy/',
'264-shy-webcam-teen-sucking-on-her-toy/',
'265-amateur-couple-fucking-at-the-dorm/',
'266-crazy-oral-sex-with-my-gf/',
'267-shy-gf-gets-fucked-hard-from-behind/',
'268-naked-chick-touching-herself/',
'269-amateur-hardcore-fucking-in-the-bedroom/',
'270-girlfriends-pussy-stuffed-hard-and-deep/',
'271-slim-chick-rides-friends-dick/',
'272-topless-webcam-cutie-flashes-her-pussy/',
'273-wild-girlfriend-fucked-while-watching-porn/',
'274-naked-slutty-babe-likes-hardcore-sex/',
'275-fucking-my-gf-in-a-kinky-nurse-outfit/',
'276-amateur-teens-having-a-wild-time-in-their-hotel-room/'];



http://galleries2.amakings.com/obsessedwithmyself/movies/225-busty-hottie-licks-tits-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/226-gorgeous-chick-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/227-bombshell-shows-off-perfect-body/
http://galleries2.amakings.com/obsessedwithmyself/movies/228-amateur-cutie-displays-her-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/229-andy-grinds-her-firm-ass/
http://galleries2.amakings.com/obsessedwithmyself/movies/230-hot-theas-super-sexy-striptease/
http://galleries2.amakings.com/obsessedwithmyself/movies/231-amateur-babes-kinky-dance/
http://galleries2.amakings.com/obsessedwithmyself/movies/232-gorgeous-chicks-nice-ass-and-boobs/
http://galleries2.amakings.com/obsessedwithmyself/movies/233-sexy-gf-shows-her-breasts-and-ass/
http://galleries2.amakings.com/obsessedwithmyself/movies/234-busty-hotties-kinky-stripdance/
http://galleries2.amakings.com/obsessedwithmyself/movies/235-sexy-babe-displays-hot-tits/
http://galleries2.amakings.com/obsessedwithmyself/movies/236-webcam-girlie-shows-huge-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/237-hotness-tasha-flashes-fine-racks/
http://galleries2.amakings.com/obsessedwithmyself/movies/238-webcam-cutie-fingerbangs-her-twat/
http://galleries2.amakings.com/obsessedwithmyself/movies/239-sexy-honey-gets-naked/
http://galleries2.amakings.com/obsessedwithmyself/movies/240-gf-strips-in-front-of-webcam/
http://galleries2.amakings.com/obsessedwithmyself/movies/241-big-titted-chicks-sexy-dance/
http://galleries2.amakings.com/obsessedwithmyself/movies/242-hottie-flashes-her-juggs/?nats=
http://galleries2.amakings.com/obsessedwithmyself/movies/243-chicks-amazing-ass-and-tits/
http://galleries2.amakings.com/obsessedwithmyself/movies/244-squeezing-her-juggs-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/245-pretty-chick-shows-her-boobs/
http://galleries2.amakings.com/obsessedwithmyself/movies/246-babe-strips-down-to-her-underwear/
http://galleries2.amakings.com/obsessedwithmyself/movies/247-flaunting-her-fine-round-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/248-naked-honey-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/249-petite-gf-flashes-her-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/250-teen-gets-naked-in-her-room/
http://galleries2.amakings.com/obsessedwithmyself/movies/251-squeezing-her-tits-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/252-nerdy-chick-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/253-blondie-playing-with-her-twat/
http://galleries2.amakings.com/obsessedwithmyself/movies/255-hot-busty-amateur-chick/
http://galleries2.amakings.com/obsessedwithmyself/movies/256-gf-strips-naked-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/257-sexy-hottie-fingers-her-cunt/
http://galleries2.amakings.com/obsessedwithmyself/movies/258-kinky-gf-gets-naked/
http://galleries2.amakings.com/obsessedwithmyself/movies/259-sexy-amateur-webcam-babe/
http://galleries2.amakings.com/obsessedwithmyself/movies/260-babe-playing-with-her-twat/
http://galleries2.amakings.com/obsessedwithmyself/movies/261-chick-puts-on-her-sexy-bikini/
http://galleries2.amakings.com/obsessedwithmyself/movies/262-webcam-cutie-in-her-bikini/
http://galleries2.amakings.com/obsessedwithmyself/movies/263-wild-gf-masturbating-hard/
http://galleries2.amakings.com/obsessedwithmyself/movies/264-busty-bombshell-spreads-on-cam/?nats=
http://galleries2.amakings.com/obsessedwithmyself/movies/265-amateur-babe-flashes-her-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/266-busty-tattooed-sexy-honey/
http://galleries2.amakings.com/obsessedwithmyself/movies/267-heavy-chested-webcam-slut/
http://galleries2.amakings.com/obsessedwithmyself/movies/268-sexy-topless-amateur-chick/
http://galleries2.amakings.com/obsessedwithmyself/movies/269-naked-sexy-babe-in-the-showers/
http://galleries2.amakings.com/obsessedwithmyself/movies/270-sexy-cutie-gets-naked/
http://galleries2.amakings.com/obsessedwithmyself/movies/271-skanky-babe-flashes-her-pussy/
http://galleries2.amakings.com/obsessedwithmyself/movies/272-busty-gf-shows-her-hot-ass/
http://galleries2.amakings.com/obsessedwithmyself/movies/273-sexy-naked-webcam-girlfriend/
http://galleries2.amakings.com/obsessedwithmyself/movies/274-gf-shakes-her-tight-round-ass/
http://galleries2.amakings.com/obsessedwithmyself/movies/275-teen-hottie-plays-with-her-pussy/
http://galleries2.amakings.com/obsessedwithmyself/movies/276-chick-playing-with-her-twat/
http://galleries2.amakings.com/obsessedwithmyself/movies/277-tattooed-babe-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/278-hot-and-sexy-naked-babe/
http://galleries2.amakings.com/obsessedwithmyself/movies/279-blonde-gf-poking-her-cunt/
http://galleries2.amakings.com/obsessedwithmyself/movies/280-hot-girlfriend-in-pink-bikini/
http://galleries2.amakings.com/obsessedwithmyself/movies/281-chick-fingers-her-pussy/
http://galleries2.amakings.com/obsessedwithmyself/movies/282-hotties-nice-tits-and-sexy-ass/
http://galleries2.amakings.com/obsessedwithmyself/movies/283-naked-webcam-chick/
http://galleries2.amakings.com/obsessedwithmyself/movies/284-slim-honey-gets-naked-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/285-sexy-girlfriend-in-a-kinky-dance/
http://galleries2.amakings.com/obsessedwithmyself/movies/286-naked-babe-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/287-hot-teen-flashing-her-tits/
http://galleries2.amakings.com/obsessedwithmyself/movies/288-pussy-play-using-a-vibrator/
http://galleries2.amakings.com/obsessedwithmyself/movies/289-topless-babe-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/290-hot-blondie-shows-her-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/291-sexy-chick-plays-with-herself/
http://galleries2.amakings.com/obsessedwithmyself/movies/292-wild-teen-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/293-pussy-play-in-the-showers/
http://galleries2.amakings.com/obsessedwithmyself/movies/294-blonde-naked-webcam-bitch/
http://galleries2.amakings.com/obsessedwithmyself/movies/295-slim-honey-teasing-her-boyfriend/
http://galleries2.amakings.com/obsessedwithmyself/movies/296-amateur-hottie-gets-topless/
http://galleries2.amakings.com/obsessedwithmyself/movies/297-horny-girlfriend-masturbating/
http://galleries2.amakings.com/obsessedwithmyself/movies/298-hot-and-sexy-webcam-babe/
http://galleries2.amakings.com/obsessedwithmyself/movies/299-horny-chick-naked-on-the-bed/
http://galleries2.amakings.com/obsessedwithmyself/movies/300-hottie-gets-naked-on-cam/
http://galleries2.amakings.com/obsessedwithmyself/movies/301-sexy-amateur-webcam-babe/
http://galleries2.amakings.com/obsessedwithmyself/movies/302-naked-chick-dildoing-her-cunt/
http://galleries2.amakings.com/obsessedwithmyself/movies/303-hottie-dancing-in-the-nude/
http://galleries2.amakings.com/obsessedwithmyself/movies/304-naked-hottie-pussy-playing/
http://galleries2.amakings.com/obsessedwithmyself/movies/305-fucking-her-twat-with-a-popsicle/
http://galleries2.amakings.com/obsessedwithmyself/movies/306-horny-webcam-gf-masturbating/?nats=
http://galleries2.amakings.com/obsessedwithmyself/movies/307-playing-with-her-shaven-twat/
http://galleries2.amakings.com/obsessedwithmyself/movies/308-amateur-girlfriend-gets-naked/
http://galleries2.amakings.com/obsessedwithmyself/movies/309-hot-babe-displays-her-breasts/
http://galleries2.amakings.com/obsessedwithmyself/movies/310-hot-amateur-webcam-girlfriend/
http://galleries2.amakings.com/obsessedwithmyself/movies/311-sexy-topless-honey/
http://galleries2.amakings.com/obsessedwithmyself/movies/312-amateur-babe-strips-naked/











http://galleries2.amakings.com/watchmygf/movies/225-horny-chick-squirts-loads/
http://galleries2.amakings.com/watchmygf/movies/226-hot-blowjob-in-cable-car/
http://galleries2.amakings.com/watchmygf/movies/227-banging-in-the-morning/
http://galleries2.amakings.com/watchmygf/movies/228-horny-sluts-masturbate-together/
http://galleries2.amakings.com/watchmygf/movies/229-girlfriend-shaves-and-masturbates/
http://galleries2.amakings.com/watchmygf/movies/230-girlfriend-films-herself-while-masturbating/
http://galleries2.amakings.com/watchmygf/movies/231-girlfriend-rides-her-boyfriends-cock-hard/








def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

sitebase = 'http://galleries2.amakings.com/obsessedwithmyself/movies/'
sitebase2 = 'http://galleries2.amakings.com/watchmygf/movies/'

checkbase = 'C:/Windows/Resources/Themes/Aero/Shell/NormalColor/en-US/New folder/'

for site in sites:
    print site
    sitefull = sitebase + site

    #create desination directory
    siteclean = string.replace(sitefull,':','')
    siteclean = string.replace(siteclean,'/','')
    filedest = 'vids/' + siteclean + '/'

    if not os.path.exists(checkbase + filedest):  
        ensure_dir(filedest)
        for i in range(1,5):
            print i
            urllib.urlretrieve (sitefull + 'videos/' + str(i) + '.wmv', filedest + str(i) + '.wmv')
     








