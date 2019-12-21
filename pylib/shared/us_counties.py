"""Patterns for US counties."""

# pylint: disable=too-many-lines

from pylib.shared import us_states
from pylib.stacked_regex.rule_catalog import RuleCatalog


CATALOG = RuleCatalog(us_states.CATALOG)


CATALOG.term('AL_co_names', r"""
    Autauga | Baldwin | Barbour | Bibb | Blount | Bullock | Butler | Calhoun
    | Chambers | Cherokee | Chilton | Choctaw | Clarke | Clay | Cleburne
    | Coffee | Colbert | Conecuh | Coosa | Covington | Crenshaw | Cullman
    | Dale | Dallas | DeKalb | Elmore | Escambia | Etowah | Fayette | Franklin
    | Geneva | Greene | Hale | Henry | Houston | Jackson | Jefferson | Lamar
    | Lauderdale | Lawrence | Lee | Limestone | Lowndes | Macon | Madison
    | Marengo | Marion | Marshall | Mobile | Monroe | Montgomery | Morgan
    | Perry | Pickens | Pike | Randolph | Russell | St\.? \s? Clair | Shelby
    | Sumter | Talladega | Tallapoosa | Tuscaloosa | Walker
    | Wilcox | Winston """)
CATALOG.grouper('AL_co', """ AL_co_names | Washington """)

CATALOG.term('AK_co_names', r"""
    Aleutians \s? East | Anchorage | Bristol \s? Bay | Denali
    | Fairbanks \s? North \s? Star | Haines | Juneau | Kenai ( \s Peninsula )?
    | Ketchikan \s? Gateway | Kodiak ( \s Island )?
    | Lake \s? and \s? Peninsula
    | Matanuska-Susitna | North \s Slope | Northwest \s Arctic | Petersburg
    | Sitka | Skagway | Wrangell | Yakutat | Unorganized | Aleutians \s West
    | Bethel | Dillingham | Hoonah-Angoon | Kusilvak | Nome
    | Prince \s? of \s? Wales-Hyder | Southeast \s? Fairbanks
    | Valdez-Cordova | Yukon-Koyukuk """)
CATALOG.grouper('AK_co', """ AK_co_names """)

CATALOG.term('AS_co_names', r"""
    Eastern ( \s District )? | Manu'a ( \s District )? | Rose ( \s Atoll )?
    | Swains ( \s Island )? | Western ( \s District )? """)
CATALOG.grouper('AS_co', """ AS_co_names """)

CATALOG.term('AZ_co_names', r"""
   Apache | Cochise | Coconino | Gila | Graham | Greenlee | La \s? Paz
   | Maricopa | Mohave | Navajo | Pima | Pinal | Santa \s? Cruz | Yavapai
   | Yuma """)
CATALOG.grouper('AZ_co', """ AZ_co_names """)

CATALOG.term('AR_co_names', r"""
    Ashley | Baxter | Benton | Boone | Bradley | Calhoun | Carroll
    | Chicot | Clark | Clay | Cleburne | Cleveland | Columbia | Conway
    | Craighead | Crawford | Crittenden | Cross | Dallas | Desha | Drew
    | Faulkner | Franklin | Fulton | Garland | Grant | Greene | Hempstead
    | Hot \s? Spring | Howard | Independence | Izard | Jackson | Jefferson
    | Johnson | Lafayette | Lawrence | Lee | Lincoln | Little \s? River | Logan
    | Lonoke | Madison | Marion | Miller | Monroe | Montgomery
    | Newton | Ouachita | Perry | Phillips | Pike | Poinsett | Polk
    | Pope | Prairie | Pulaski | Randolph | St\.? \s? Francis | Saline | Scott
    | Searcy | Sebastian | Sevier | Sharp | Stone | Union | Van \s? Buren
    | White | Woodruff | Yell """)
CATALOG.grouper('AR_co', """
    AR_co_names | Arkansas | Mississippi | Nevada | Washington  """)

CATALOG.term('CA_co_names', r"""
    Alameda | Alpine | Amador | Butte | Calaveras | Colusa | Contra \s? Costa
    | Del \s? Norte | El \s? Dorado | Fresno | Glenn | Humboldt | Imperial
    | Inyo | Kern | Kings | Lake | Lassen | Los \s? Angeles | Madera | Marin
    | Mariposa | Mendocino | Merced | Modoc | Mono | Monterey | Napa
    | Orange | Placer | Plumas | Riverside | Sacramento | San \s? Benito
    | San \s? Bernardino | San \s? Diego | San \s? Francisco | San \s? Joaquin
    | San \s? Luis \s? Obispo | San \s? Mateo | Santa \s? Barbara
    | Santa \s? Clara | Santa \s? Cruz | Shasta | Sierra | Siskiyou | Solano
    | Sonoma | Stanislaus | Sutter | Tehama | Trinity | Tulare | Tuolumne
    | Ventura | Yolo | Yuba """)
CATALOG.grouper('CA_co', """ CA_co_names | Nevada """)

CATALOG.term('CO_co_names', r"""
    Adams | Alamosa | Arapahoe | Archuleta | Baca | Bent | Boulder | Broomfield
    | Chaffee | Cheyenne | Clear \s? Creek | Conejos | Costilla | Crowley
    | Custer | Delta | Denver | Dolores | Douglas | Eagle | Elbert
    | El \s? Paso | Fremont | Garfield | Gilpin | Grand | Gunnison | Hinsdale
    | Huerfano | Jackson | Jefferson | Kiowa | Kit \s? Carson | Lake
    | La \s? Plata | Larimer | Las \s? Animas | Lincoln | Logan | Mesa
    | Mineral | Moffat | Montezuma | Montrose | Morgan | Otero | Ouray | Park
    | Phillips | Pitkin | Prowers | Pueblo | Rio \s? Blanco | Rio \s? Grande
    | Routt | Saguache | San \s? Juan | San \s? Miguel | Sedgwick | Summit
    | Teller | Weld | Yuma """)
CATALOG.grouper('CO_co', """ CO_co_names | Washington """)

CATALOG.term('CT_co_names', r"""
    Fairfield | Hartford | Litchfield | Middlesex | New \s? Haven
    | New \s? London | Tolland | Windham """)
CATALOG.grouper('CT_co', """ CT_co_names """)

CATALOG.term('DE_co_names', r""" Kent | New \s? Castle | Sussex """)
CATALOG.grouper('DE_co', """ DE_co_names """)

CATALOG.term('DC_co_names', r""" District \s? of \s? Columbia """)
CATALOG.grouper('DC_co', """ DC_co_names """)

CATALOG.term('FL_co_names', r"""
    Alachua | Baker | Bay | Bradford | Brevard | Broward | Calhoun | Charlotte
    | Citrus | Clay | Collier | Columbia | DeSoto | Dixie | Duval | Escambia
    | Flagler | Franklin | Gadsden | Gilchrist | Glades | Gulf | Hamilton
    | Hardee | Hendry | Hernando | Highlands | Hillsborough | Holmes
    | Indian \s? River | Jackson | Jefferson | Lafayette | Lake | Lee | Leon
    | Levy | Liberty | Madison | Manatee | Marion | Martin | Miami-Dade
    | Monroe | Nassau | Okaloosa | Okeechobee | Orange | Osceola
    | Palm \s? Beach | Pasco | Pinellas | Polk | Putnam | St\.? \s? Johns
    | St\.? \s? Lucie | Santa \s? Rosa | Sarasota | Seminole | Sumter
    | Suwannee | Taylor | Union | Volusia | Wakulla | Walton """)
CATALOG.grouper('FL_co', """ FL_co_names | Washington """)

CATALOG.term('GA_co_names', r"""
    Appling | Atkinson | Bacon | Baker | Baldwin | Banks | Barrow | Bartow
    | Ben \s? Hill | Berrien | Bibb | Bleckley | Brantley | Brooks | Bryan
    | Bulloch | Burke | Butts | Calhoun | Camden | Candler | Carroll | Catoosa
    | Charlton | Chatham | Chattahoochee | Chattooga | Cherokee | Clarke | Clay
    | Clayton | Clinch | Cobb | Coffee | Colquitt | Columbia | Cook | Coweta
    | Crawford | Crisp | Dade | Dawson | Decatur | DeKalb | Dodge | Dooly
    | Dougherty | Douglas | Early | Echols | Effingham | Elbert | Emanuel
    | Evans | Fannin | Fayette | Floyd | Forsyth | Franklin | Fulton | Gilmer
    | Glascock | Glynn | Gordon | Grady | Greene | Gwinnett | Habersham | Hall
    | Hancock | Haralson | Harris | Hart | Heard | Henry | Houston | Irwin
    | Jackson | Jasper | Jeff \s? Davis | Jefferson | Jenkins | Johnson
    | Jones | Lamar | Lanier | Laurens | Lee | Liberty | Lincoln | Long
    | Lowndes | Lumpkin | McDuffie | McIntosh | Macon | Madison | Marion
    | Meriwether | Miller | Mitchell | Monroe | Montgomery | Morgan | Murray
    | Muscogee | Newton | Oconee | Oglethorpe | Paulding | Peach | Pickens
    | Pierce | Pike | Polk | Pulaski | Putnam | Quitman | Rabun | Randolph
    | Richmond | Rockdale | Schley | Screven | Seminole | Spalding | Stephens
    | Stewart | Sumter | Talbot | Taliaferro | Tattnall | Taylor | Telfair
    | Terrell | Thomas | Tift | Toombs | Towns | Treutlen | Troup | Turner
    | Twiggs | Union | Upson | Walker | Walton | Ware | Warren
    | Wayne | Webster | Wheeler | White | Whitfield | Wilcox | Wilkes
    | Wilkinson | Worth """)
CATALOG.grouper('GA_co', """ GA_co_names | Washington """)

CATALOG.term('GU_co_names', r""" Guam """)
CATALOG.grouper('GU_co', """ GU_co_names """)

CATALOG.term('HI_co_names', r""" Honolulu | Kalawao | Kauai | Maui """)
CATALOG.grouper('HI_co', """ HI_co_names | Hawaii """)

CATALOG.term('ID_co_names', r"""
    Ada | Adams | Bannock | Bear \s? Lake | Benewah | Bingham | Blaine | Boise
    | Bonner | Bonneville | Boundary | Butte | Camas | Canyon | Caribou
    | Cassia | Clark | Clearwater | Custer | Elmore | Franklin | Fremont
    | Gem | Gooding | Jefferson | Jerome | Kootenai | Latah | Lemhi
    | Lewis | Lincoln | Madison | Minidoka | Nez \s? Perce | Oneida | Owyhee
    | Payette | Power | Shoshone | Teton | Twin \s? Falls | Valley """)
CATALOG.grouper('ID_co', """ ID_co_names | Idaho | Washington  """)

CATALOG.term('IL_co_names', r"""
    Adams | Alexander | Bond | Boone | Brown | Bureau | Calhoun | Carroll
    | Cass | Champaign | Christian | Clark | Clay | Clinton | Coles | Cook
    | Crawford | Cumberland | DeKalb | De \s? Witt | Douglas | DuPage | Edgar
    | Edwards | Effingham | Fayette | Ford | Franklin | Fulton | Gallatin
    | Greene | Grundy | Hamilton | Hancock | Hardin | Henderson | Henry
    | Iroquois | Jackson | Jasper | Jefferson | Jersey | Jo \s? Daviess
    | Johnson | Kane | Kankakee | Kendall | Knox | Lake | LaSalle | Lawrence
    | Lee | Livingston | Logan | McDonough | McHenry | McLean | Macon
    | Macoupin | Madison | Marion | Marshall | Mason | Massac | Menard
    | Mercer | Monroe | Montgomery | Morgan | Moultrie | Ogle | Peoria | Perry
    | Piatt | Pike | Pope | Pulaski | Putnam | Randolph | Richland
    | Rock ( \s Island )? | St\.? \s? Clair | Saline | Sangamon | Schuyler
    | Scott | Shelby | Stark | Stephenson | Tazewell | Union | Vermilion
    | Wabash | Warren | Wayne | White | Whiteside | Will
    | Williamson | Winnebago | Woodford """)
CATALOG.grouper('IL_co', """ IL_co_names | Washington """)

CATALOG.term('IN_co_names', r"""
    Adams | Allen | Bartholomew | Benton | Blackford | Boone | Brown | Carroll
    | Cass | Clark | Clay | Clinton | Crawford | Daviess | Dearborn | Decatur
    | DeKalb | Dubois | Elkhart | Fayette | Floyd | Fountain
    | Franklin | Fulton | Gibson | Grant | Greene | Hamilton | Hancock
    | Harrison | Hendricks | Henry | Howard | Huntington | Jackson | Jasper
    | Jay | Jefferson | Jennings | Johnson | Knox | Kosciusko | LaGrange
    | Lake | LaPorte | Lawrence | Madison | Marion | Marshall | Martin | Miami
    | Monroe | Montgomery | Morgan | Newton | Noble | Orange | Owen
    | Parke | Perry | Pike | Porter | Posey | Pulaski | Putnam | Randolph
    | Ripley | Rush | St\.? \s? Joseph | Scott | Shelby | Spencer | Starke
    | Steuben | Sullivan | Switzerland | Tippecanoe | Tipton | Union
    | Vanderburgh | Vermillion | Vigo | Wabash | Warren | Warrick
    | Wayne | Wells | White | Whitley """)
CATALOG.grouper('IN_co', """ IN_co_names | Delaware | Ohio | Washington """)

CATALOG.term('IA_co_names', r"""
    Adair | Adams | Allamakee | Appanoose | Audubon | Benton | Black \s? Hawk
    | Boone | Bremer | Buchanan | Buena \s? Vista | Butler | Calhoun | Carroll
    | Cass | Cedar | Cerro \s? Gordo | Cherokee | Chickasaw | Clarke | Clay
    | Clayton | Clinton | Crawford | Dallas | Davis | Decatur
    | Des \s? Moines | Dickinson | Dubuque | Emmet | Fayette | Floyd | Franklin
    | Fremont | Greene | Grundy | Guthrie | Hamilton | Hancock | Hardin
    | Harrison | Henry | Howard | Humboldt | Ida | Jackson | Jasper
    | Jefferson | Johnson | Jones | Keokuk | Kossuth | Lee | Linn | Louisa
    | Lucas | Lyon | Madison | Mahaska | Marion | Marshall | Mills | Mitchell
    | Monona | Monroe | Montgomery | Muscatine | O'Brien | Osceola | Page
    | Palo \s? Alto | Plymouth | Pocahontas | Polk | Pottawattamie | Poweshiek
    | Ringgold | Sac | Scott | Shelby | Sioux | Story | Tama | Taylor | Union
    | Van \s? Buren | Wapello | Warren | Wayne | Webster
    | Winnebago | Winneshiek | Woodbury | Worth | Wright """)
CATALOG.grouper('IA_co', """ IA_co_names | Delaware | Iowa | Washington """)

CATALOG.term('KS_co_names', r"""
    Allen | Anderson | Atchison | Barber | Barton | Bourbon | Brown | Butler
    | Chase | Chautauqua | Cherokee | Cheyenne | Clark | Clay | Cloud | Coffey
    | Comanche | Cowley | Crawford | Decatur | Dickinson | Doniphan | Douglas
    | Edwards | Elk | Ellis | Ellsworth | Finney | Ford | Franklin | Geary
    | Gove | Graham | Grant | Gray | Greeley | Greenwood | Hamilton | Harper
    | Harvey | Haskell | Hodgeman | Jackson | Jefferson | Jewell | Johnson
    | Kearny | Kingman | Kiowa | Labette | Lane | Leavenworth | Lincoln | Linn
    | Logan | Lyon | McPherson | Marion | Marshall | Meade | Miami | Mitchell
    | Montgomery | Morris | Morton | Nemaha | Neosho | Ness | Norton | Osage
    | Osborne | Ottawa | Pawnee | Phillips | Pottawatomie | Pratt | Rawlins
    | Reno | Republic | Rice | Riley | Rooks | Rush | Russell | Saline | Scott
    | Sedgwick | Seward | Shawnee | Sheridan | Sherman | Smith | Stafford
    | Stanton | Stevens | Sumner | Thomas | Trego | Wabaunsee | Wallace
    | Wichita | Wilson | Woodson | Wyandotte """)
CATALOG.grouper('KS_co', """ KS_co_names | Washington """)

CATALOG.term('KY_co_names', r"""
    Adair | Allen | Anderson | Ballard | Barren | Bath | Bell | Boone | Bourbon
    | Boyd | Boyle | Bracken | Breathitt | Breckinridge | Bullitt | Butler
    | Caldwell | Calloway | Campbell | Carlisle | Carroll | Carter | Casey
    | Christian | Clark | Clay | Clinton | Crittenden | Cumberland | Daviess
    | Edmonson | Elliott | Estill | Fayette | Fleming | Floyd | Franklin
    | Fulton | Gallatin | Garrard | Grant | Graves | Grayson | Green
    | Greenup | Hancock | Hardin | Harlan | Harrison | Hart | Henderson
    | Henry | Hickman | Hopkins | Jackson | Jefferson | Jessamine | Johnson
    | Kenton | Knott | Knox | LaRue | Laurel | Lawrence | Lee | Leslie
    | Letcher | Lewis | Lincoln | Livingston | Logan | Lyon | McCracken
    | McCreary | McLean | Madison | Magoffin | Marion | Marshall | Martin
    | Mason | Meade | Menifee | Mercer | Metcalfe | Monroe | Montgomery
    | Morgan | Muhlenberg | Nelson | Nicholas | Oldham | Owen | Owsley
    | Pendleton | Perry | Pike | Powell | Pulaski | Robertson | Rockcastle
    | Rowan | Russell | Scott | Shelby | Simpson | Spencer | Taylor | Todd
    | Trigg | Trimble | Union | Warren | Wayne | Webster | Whitley
    | Wolfe | Woodford """)
CATALOG.grouper('KY_co', """ KY_co_names | Ohio | Washington """)

CATALOG.term('LA_co_names', r"""
    Acadia | Allen | Ascension | Assumption | Avoyelles | Beauregard
    | Bienville | Bossier | Caddo | Calcasieu | Caldwell | Cameron | Catahoula
    | Claiborne | Concordia | De \s? Soto | East \s? Baton \s? Rouge
    | East \s? Carroll | East \s? Feliciana | Evangeline | Franklin | Grant
    | Iberia | Iberville | Jackson | Jefferson | Jefferson \s? Davis
    | Lafayette | Lafourche | La \s? Salle | Lincoln | Livingston | Madison
    | Morehouse | Natchitoches | Orleans | Ouachita | Plaquemines
    | Pointe \s? Coupee | Rapides | Red \s? River | Richland | Sabine
    | St\.? \s? Bernard | St\.? \s? Charles | St\.? \s? Helena
    | St\.? \s? James | St\.? \s? John \s? the \s? Baptist | St\.? \s? Landry
    | St\.? \s? Martin | St\.? \s? Mary | St\.? \s? Tammany | Tangipahoa
    | Tensas | Terrebonne | Union | Vermilion | Vernon | Webster
    | West \s? Baton \s? Rouge | West \s? Carroll | West \s? Feliciana
    | Winn """)
CATALOG.grouper('LA_co', """ LA_co_names | Washington """)

CATALOG.term('ME_co_names', r"""
    Androscoggin | Aroostook | Cumberland | Franklin | Hancock | Kennebec
    | Knox | Lincoln | Oxford | Penobscot | Piscataquis | Sagadahoc | Somerset
    | Waldo | York """)
CATALOG.grouper('ME_co', """ ME_co_names | Washington """)

CATALOG.term('MD_co_names', r"""
    Allegany | Anne \s? Arundel | Baltimore | Calvert | Caroline | Carroll
    | Cecil | Charles | Dorchester | Frederick | Garrett | Harford | Howard
    | Kent | Montgomery | Prince \s? George's | Queen \s? Anne's
    | St\.? \s? Mary's | Somerset | Talbot | Wicomico | Worcester
    | Baltimore """)
CATALOG.grouper('MD_co', """ MD_co_names | Washington """)

CATALOG.term('MA_co_names', r"""
    Barnstable | Berkshire | Bristol | Dukes | Essex | Franklin | Hampden
    | Hampshire | Middlesex | Nantucket | Norfolk | Plymouth | Suffolk
    | Worcester """)
CATALOG.grouper('MA_co', """ MA_co_names """)

CATALOG.term('MI_co_names', r"""
    Alcona | Alger | Allegan | Alpena | Antrim | Arenac | Baraga | Barry | Bay
    | Benzie | Berrien | Branch | Calhoun | Cass | Charlevoix | Cheboygan
    | Chippewa | Clare | Clinton | Crawford | Delta | Dickinson | Eaton | Emmet
    | Genesee | Gladwin | Gogebic | Grand \s? Traverse | Gratiot | Hillsdale
    | Houghton | Huron | Ingham | Ionia | Iosco | Iron | Isabella | Jackson
    | Kalamazoo | Kalkaska | Kent | Keweenaw | Lake | Lapeer | Leelanau
    | Lenawee | Livingston | Luce | Mackinac | Macomb | Manistee | Marquette
    | Mason | Mecosta | Menominee | Midland | Missaukee | Monroe | Montcalm
    | Montmorency | Muskegon | Newaygo | Oakland | Oceana | Ogemaw | Ontonagon
    | Osceola | Oscoda | Otsego | Ottawa | Presque \s? Isle | Roscommon
    | Saginaw | St\.? \s? Clair | St\.? \s? Joseph | Sanilac | Schoolcraft
    | Shiawassee | Tuscola | Van \s? Buren | Washtenaw | Wayne | Wexford """)
CATALOG.grouper('MI_co', """ MI_co_names """)

CATALOG.term('MN_co_names', r"""
    Aitkin | Anoka | Becker | Beltrami | Benton | Big \s? Stone
    | Blue \s? Earth | Brown | Carlton | Carver | Cass | Chippewa | Chisago
    | Clay | Clearwater | Cook | Cottonwood | Crow \s? Wing | Dakota | Dodge
    | Douglas | Faribault | Fillmore | Freeborn | Goodhue | Grant | Hennepin
    | Houston | Hubbard | Isanti | Itasca | Jackson | Kanabec | Kandiyohi
    | Kittson | Koochiching | Lac \s? qui \s? Parle | Lake
    | Lake \s? of \s? the \s? Woods | Le \s? Sueur | Lincoln | Lyon | McLeod
    | Mahnomen | Marshall | Martin | Meeker | Mille \s? Lacs | Morrison | Mower
    | Murray | Nicollet | Nobles | Norman | Olmsted | Otter \s? Tail
    | Pennington | Pine | Pipestone | Polk | Pope | Ramsey | Red \s? Lake
    | Redwood | Renville | Rice | Rock | Roseau | St\.? \s? Louis | Scott
    | Sherburne | Sibley | Stearns | Steele | Stevens | Swift | Todd
    | Traverse | Wabasha | Wadena | Waseca | Watonwan | Wilkin
    | Winona | Wright | Yellow \s? Medicine """)
CATALOG.grouper('MN_co', """ MN_co_names | Washington """)

CATALOG.term('MS_co_names', r"""
    Adams | Alcorn | Amite | Attala | Benton | Bolivar | Calhoun | Carroll
    | Chickasaw | Choctaw | Claiborne | Clarke | Clay | Coahoma | Copiah
    | Covington | DeSoto | Forrest | Franklin | George | Greene | Grenada
    | Hancock | Harrison | Hinds | Holmes | Humphreys | Issaquena | Itawamba
    | Jackson | Jasper | Jefferson | Jefferson \s? Davis | Jones | Kemper
    | Lafayette | Lamar | Lauderdale | Lawrence | Leake | Lee | Leflore
    | Lincoln | Lowndes | Madison | Marion | Marshall | Monroe | Montgomery
    | Neshoba | Newton | Noxubee | Oktibbeha | Panola | Pearl \s? River | Perry
    | Pike | Pontotoc | Prentiss | Quitman | Rankin | Scott | Sharkey | Simpson
    | Smith | Stone | Sunflower | Tallahatchie | Tate | Tippah | Tishomingo
    | Tunica | Union | Walthall | Warren | Wayne | Webster
    | Wilkinson | Winston | Yalobusha | Yazoo """)
CATALOG.grouper('MS_co', """ MS_co_names | Washington""")

CATALOG.term('MO_co_names', r"""
    Adair | Andrew | Atchison | Audrain | Barry | Barton | Bates | Benton
    | Bollinger | Boone | Buchanan | Butler | Caldwell | Callaway | Camden
    | Cape \s? Girardeau | Carroll | Carter | Cass | Cedar | Chariton
    | Christian | Clark | Clay | Clinton | Cole | Cooper | Crawford | Dade
    | Dallas | Daviess | DeKalb | Dent | Douglas | Dunklin | Franklin
    | Gasconade | Gentry | Greene | Grundy | Harrison | Henry | Hickory | Holt
    | Howard | Howell | Iron | Jackson | Jasper | Jefferson | Johnson | Knox
    | Laclede | Lafayette | Lawrence | Lewis | Lincoln | Linn | Livingston
    | McDonald | Macon | Madison | Maries | Marion | Mercer | Miller
    | Moniteau | Monroe | Montgomery | Morgan | New \s? Madrid
    | Newton | Nodaway | Osage | Ozark | Pemiscot | Perry | Pettis
    | Phelps | Pike | Platte | Polk | Pulaski | Putnam | Ralls | Randolph | Ray
    | Reynolds | Ripley | St\.? \s? Charles | St\.? \s? Clair
    | Ste\.? \s? Genevieve | St\.? \s? Francois | St\.? \s? Louis | Saline
    | Schuyler | Scotland | Scott | Shannon | Shelby | Stoddard | Stone
    | Sullivan | Taney | Vernon | Warren | Wayne
    | Webster | Worth | Wright """)
CATALOG.grouper('MO_co', """
    MO_co_names | Mississippi | Oregon | Texas | Washington """)

CATALOG.term('MT_co_names', r"""
    Beaverhead | Big \s? Horn | Blaine | Broadwater | Carbon | Carter
    | Cascade | Chouteau | Custer | Daniels | Dawson | Deer \s? Lodge
    | Fallon | Fergus | Flathead | Gallatin | Garfield | Glacier
    | Golden \s? Valley | Granite | Hill | Jefferson | Judith \s? Basin
    | Lake | Lewis \s? and \s? Clark | Liberty | Lincoln | McCone | Madison
    | Meagher | Mineral | Missoula | Musselshell | Park | Petroleum | Phillips
    | Pondera | Powder \s? River | Powell | Prairie | Ravalli | Richland
    | Roosevelt | Rosebud | Sanders | Sheridan | Silver \s? Bow | Stillwater
    | Sweet \s? Grass | Teton | Toole | Treasure | Valley | Wheatland
    | Wibaux | Yellowstone """)
CATALOG.grouper('MT_co', """ MT_co_names """)

CATALOG.term('NE_co_names', r"""
    Adams | Antelope | Arthur | Banner | Blaine | Boone | Box \s? Butte | Boyd
    | Brown | Buffalo | Burt | Butler | Cass | Cedar | Chase | Cherry
    | Cheyenne | Clay | Colfax | Cuming | Custer | Dakota | Dawes | Dawson
    | Deuel | Dixon | Dodge | Douglas | Dundy | Fillmore | Franklin | Frontier
    | Furnas | Gage | Garden | Garfield | Gosper | Grant | Greeley | Hall
    | Hamilton | Harlan | Hayes | Hitchcock | Holt | Hooker | Howard
    | Jefferson | Johnson | Kearney | Keith | Keya \s? Paha | Kimball | Knox
    | Lancaster | Lincoln | Logan | Loup | McPherson | Madison | Merrick
    | Morrill | Nance | Nemaha | Nuckolls | Otoe | Pawnee | Perkins | Phelps
    | Pierce | Platte | Polk | Red \s? Willow | Richardson | Rock | Saline
    | Sarpy | Saunders | Scotts \s? Bluff | Seward | Sheridan | Sherman
    | Sioux | Stanton | Thayer | Thomas | Thurston | Valley
    | Wayne | Webster | Wheeler | York """)
CATALOG.grouper('NE_co', """ NE_co_names | Washington """)

CATALOG.term('NV_co_names', r"""
    Carson \s? City | Churchill | Clark | Douglas | Elko | Esmeralda | Eureka
    | Humboldt | Lander | Lincoln | Lyon | Mineral | Nye | Pershing | Storey
    | Washoe | White \s? Pine """)
CATALOG.grouper('NV_co', """ NV_co_names """)

CATALOG.term('NH_co_names', r"""
    Belknap | Carroll | Cheshire | Coös | Grafton | Hillsborough | Merrimack
    | Rockingham | Strafford | Sullivan """)
CATALOG.grouper('NH_co', """ NH_co_names """)

CATALOG.term('NJ_co_names', r"""
    Atlantic | Bergen | Burlington | Camden | Cape \s? May | Cumberland | Essex
    | Gloucester | Hudson | Hunterdon | Mercer | Middlesex | Monmouth | Morris
    | Ocean | Passaic | Salem | Somerset | Sussex | Union | Warren """)
CATALOG.grouper('NJ_co', """ NJ_co_names """)

CATALOG.term('NM_co_names', r"""
    Bernalillo | Catron | Chaves | Cibola | Colfax | Curry | De \s? Baca
    | Doña \s? Ana | Eddy | Grant | Guadalupe | Harding | Hidalgo | Lea
    | Lincoln | Los \s? Alamos | Luna | McKinley | Mora | Otero | Quay
    | Rio \s? Arriba | Roosevelt | Sandoval | San \s? Juan | San \s? Miguel
    | Santa \s? Fe | Sierra | Socorro | Taos | Torrance | Union | Valencia """)
CATALOG.grouper('NM_co', """ NM_co_names """)

CATALOG.term('NY_co_names', r"""
    Albany | Allegany | Bronx | Broome | Cattaraugus | Cayuga | Chautauqua
    | Chemung | Chenango | Clinton | Columbia | Cortland | Dutchess
    | Erie | Essex | Franklin | Fulton | Genesee | Greene | Hamilton | Herkimer
    | Jefferson | Kings | Lewis | Livingston | Madison | Monroe | Montgomery
    | Nassau | Niagara | Oneida | Onondaga | Ontario | Orange
    | Orleans | Oswego | Otsego | Putnam | Queens | Rensselaer | Richmond
    | Rockland | St\.? \s? Lawrence | Saratoga | Schenectady | Schoharie
    | Schuyler | Seneca | Steuben | Suffolk | Sullivan | Tioga | Tompkins
    | Ulster | Warren | Wayne | Westchester | Yates """)
CATALOG.grouper('NY_co', """
    NY_co_names | Delaware| New_York | Washington | Wyoming """)

CATALOG.term('NC_co_names', r"""
    Alamance | Alexander | Alleghany | Anson | Ashe | Avery | Beaufort | Bertie
    | Bladen | Brunswick | Buncombe | Burke | Cabarrus | Caldwell | Camden
    | Carteret | Caswell | Catawba | Chatham | Cherokee | Chowan | Clay
    | Cleveland | Columbus | Craven | Cumberland | Currituck | Dare | Davidson
    | Davie | Duplin | Durham | Edgecombe | Forsyth | Franklin | Gaston | Gates
    | Graham | Granville | Greene | Guilford | Halifax | Harnett | Haywood
    | Henderson | Hertford | Hoke | Hyde | Iredell | Jackson | Johnston | Jones
    | Lee | Lenoir | Lincoln | McDowell | Macon | Madison | Martin
    | Mecklenburg | Mitchell | Montgomery | Moore | Nash | New \s? Hanover
    | Northampton | Onslow | Orange | Pamlico | Pasquotank | Pender
    | Perquimans | Person | Pitt | Polk | Randolph | Richmond | Robeson
    | Rockingham | Rowan | Rutherford | Sampson | Scotland | Stanly | Stokes
    | Surry | Swain | Transylvania | Tyrrell | Union | Vance | Wake | Warren
    | Watauga | Wayne | Wilkes | Wilson | Yadkin | Yancey """)
CATALOG.grouper('NC_co', """ NC_co_names | Washington """)

CATALOG.term('ND_co_names', r"""
    Adams | Barnes | Benson | Billings | Bottineau | Bowman | Burke
    | Burleigh | Cass | Cavalier | Dickey | Divide | Dunn | Eddy | Emmons
    | Foster | Golden \s? Valley | Grand \s? Forks | Grant | Griggs | Hettinger
    | Kidder | LaMoure | Logan | McHenry | McIntosh | McKenzie | McLean
    | Mercer | Morton | Mountrail | Nelson | Oliver | Pembina | Pierce | Ramsey
    | Ransom | Renville | Richland | Rolette | Sargent | Sheridan | Sioux
    | Slope | Stark | Steele | Stutsman | Towner | Traill | Walsh | Ward
    | Wells | Williams """)
CATALOG.grouper('ND_co', """ ND_co_names """)

CATALOG.term(
    'MP_co_names', r""" Northern \s? Islands | Rota | Saipan | Tinian """)
CATALOG.grouper('MP_co', """ MP_co_names """)

CATALOG.term('OH_co_names', r"""
    Adams | Allen | Ashland | Ashtabula | Athens | Auglaize | Belmont | Brown
    | Butler | Carroll | Champaign | Clark | Clermont | Clinton | Columbiana
    | Coshocton | Crawford | Cuyahoga | Darke | Defiance | Erie
    | Fairfield | Fayette | Franklin | Fulton | Gallia | Geauga | Greene
    | Guernsey | Hamilton | Hancock | Hardin | Harrison | Henry | Highland
    | Hocking | Holmes | Huron | Jackson | Jefferson | Knox | Lake | Lawrence
    | Licking | Logan | Lorain | Lucas | Madison | Mahoning | Marion | Medina
    | Meigs | Mercer | Miami | Monroe | Montgomery | Morgan | Morrow
    | Muskingum | Noble | Ottawa | Paulding | Perry | Pickaway | Pike | Portage
    | Preble | Putnam | Richland | Ross | Sandusky | Scioto | Seneca | Shelby
    | Stark | Summit | Trumbull | Tuscarawas | Union | Van \s? Wert | Vinton
    | Warren | Wayne | Williams | Wood | Wyandot """)
CATALOG.grouper('OH_co', """ OH_co_names | Delaware | Washington """)

CATALOG.term('OK_co_names', r"""
    Adair | Alfalfa | Atoka | Beaver | Beckham | Blaine | Bryan | Caddo
    | Canadian | Carter | Cherokee | Choctaw | Cimarron | Cleveland | Coal
    | Comanche | Cotton | Craig | Creek | Custer | Dewey | Ellis
    | Garfield | Garvin | Grady | Grant | Greer | Harmon | Harper | Haskell
    | Hughes | Jackson | Jefferson | Johnston | Kay | Kingfisher | Kiowa
    | Latimer | Le \s? Flore | Lincoln | Logan | Love | McClain | McCurtain
    | McIntosh | Major | Marshall | Mayes | Murray | Muskogee | Noble | Nowata
    | Okfuskee | Okmulgee | Osage | Ottawa | Pawnee | Payne
    | Pittsburg | Pontotoc | Pottawatomie | Pushmataha | Roger \s? Mills
    | Rogers | Seminole | Sequoyah | Stephens | Tillman | Tulsa
    | Wagoner | Washita | Woods | Woodward """)
CATALOG.grouper('OK_co', """
    OK_co_names | Delaware | Oklahoma | Texas | Washington  """)

CATALOG.term('OR_co_names', r"""
    Baker | Benton | Clackamas | Clatsop | Columbia | Coos | Crook | Curry
    | Deschutes | Douglas | Gilliam | Grant | Harney | Hood \s? River | Jackson
    | Jefferson | Josephine | Klamath | Lake | Lane | Lincoln | Linn | Malheur
    | Marion | Morrow | Multnomah | Polk | Sherman | Tillamook | Umatilla
    | Union | Wallowa | Wasco | Wheeler | Yamhill """)
CATALOG.grouper('OR_co', """ OR_co_names | Washington """)

CATALOG.term('PA_co_names', r"""
    Adams | Allegheny | Armstrong | Beaver | Bedford | Berks | Blair | Bradford
    | Bucks | Butler | Cambria | Cameron | Carbon | Centre | Chester | Clarion
    | Clearfield | Clinton | Columbia | Crawford | Cumberland | Dauphin
    | Elk | Erie | Fayette | Forest | Franklin | Fulton | Greene
    | Huntingdon | Jefferson | Juniata | Lackawanna | Lancaster
    | Lawrence | Lebanon | Lehigh | Luzerne | Lycoming | McKean | Mercer
    | Mifflin | Monroe | Montgomery | Montour | Northampton | Northumberland
    | Perry | Philadelphia | Pike | Potter | Schuylkill | Snyder | Somerset
    | Sullivan | Susquehanna | Tioga | Union | Venango | Warren
    | Wayne | Westmoreland | York """)
CATALOG.grouper('PA_co', """
    PA_co_names | Delaware | Indiana | Washington | Wyoming """)

CATALOG.term('PR_co_names', r"""
    Adjuntas | Aguada | Aguadilla | Aguas \s? Buenas | Aibonito | Añasco
    | Arecibo | Arroyo | Barceloneta | Barranquitas | Bayamón | Cabo \s? Rojo
    | Caguas | Camuy | Canóvanas | Carolina | Cataño | Cayey | Ceiba | Ciales
    | Cidra | Coamo | Comerío | Corozal | Culebra | Dorado | Fajardo
    | Guánica | Guayama | Guayanilla | Guaynabo | Gurabo | Hatillo
    | Hormigueros | Humacao | Isabela | Jayuya | Juana \s? Díaz | Juncos
    | Lajas | Lares | Las \s? Marías | Las \s? Piedras | Loíza | Luquillo
    | Manatí | Maricao | Maunabo | Mayagüez | Moca | Morovis | Naguabo
    | Naranjito | Orocovis | Patillas | Peñuelas | Ponce | Quebradillas
    | Rincón | Río \s? Grande | Sabana \s? Grande | Salinas | San \s? Germán
    | San \s? Juan | San \s? Lorenzo | San \s? Sebastián | Santa \s? Isabel
    | Toa \s? Alta | Toa \s? Baja | Trujillo \s? Alto | Utuado | Vega \s? Alta
    | Vega \s? Baja | Vieques | Villalba | Yabucoa | Yauco """)
CATALOG.grouper('PR_co', """ PR_co_names | Florida """)

CATALOG.term('RI_co_names', r""" Kent | Newport | Providence """)
CATALOG.grouper('RI_co', """ RI_co_names | Washington """)

CATALOG.term('SC_co_names', r"""
    Abbeville | Aiken | Allendale | Anderson | Bamberg | Barnwell | Beaufort
    | Berkeley | Calhoun | Charleston | Cherokee | Chester | Chesterfield
    | Clarendon | Colleton | Darlington | Dillon | Dorchester | Edgefield
    | Fairfield | Florence | Georgetown | Greenville | Greenwood | Hampton
    | Horry | Jasper | Kershaw | Lancaster | Laurens | Lee | Lexington
    | McCormick | Marion | Marlboro | Newberry | Oconee | Orangeburg | Pickens
    | Richland | Saluda | Spartanburg | Sumter | Union | Williamsburg
    | York """)
CATALOG.grouper('SC_co', """ SC_co_names """)

CATALOG.term('SD_co_names', r"""
    Aurora | Beadle | Bennett | Bon \s? Homme | Brookings | Brown | Brule
    | Buffalo | Butte | Campbell | Charles \s? Mix | Clark | Clay | Codington
    | Corson | Custer | Davison | Day | Deuel | Dewey | Douglas | Edmunds
    | Fall \s? River | Faulk | Grant | Gregory | Haakon | Hamlin | Hand
    | Hanson | Harding | Hughes | Hutchinson | Hyde | Jackson | Jerauld | Jones
    | Kingsbury | Lake | Lawrence | Lincoln | Lyman | McCook | McPherson
    | Marshall | Meade | Mellette | Miner | Minnehaha | Moody
    | Oglala \s? Lakota | Pennington | Perkins | Potter | Roberts | Sanborn
    | Spink | Stanley | Sully | Todd | Tripp | Turner | Union | Walworth
    | Yankton | Ziebach """)
CATALOG.grouper('SD_co', """ SD_co_names """)

CATALOG.term('TN_co_names', r"""
    Anderson | Bedford | Benton | Bledsoe | Blount | Bradley | Campbell
    | Cannon | Carroll | Carter | Cheatham | Chester | Claiborne | Clay
    | Cocke | Coffee | Crockett | Cumberland | Davidson | Decatur | DeKalb
    | Dickson | Dyer | Fayette | Fentress | Franklin | Gibson | Giles
    | Grainger | Greene | Grundy | Hamblen | Hamilton | Hancock | Hardeman
    | Hardin | Hawkins | Haywood | Henderson | Henry | Hickman | Houston
    | Humphreys | Jackson | Jefferson | Johnson | Knox | Lake | Lauderdale
    | Lawrence | Lewis | Lincoln | Loudon | McMinn | McNairy | Macon | Madison
    | Marion | Marshall | Maury | Meigs | Monroe | Montgomery | Moore | Morgan
    | Obion | Overton | Perry | Pickett | Polk | Putnam | Rhea | Roane
    | Robertson | Rutherford | Scott | Sequatchie | Sevier | Shelby | Smith
    | Stewart | Sullivan | Sumner | Tipton | Trousdale | Unicoi | Union
    | Van \s? Buren | Warren | Wayne | Weakley | White
    | Williamson """)
CATALOG.grouper('TN_co', """ TN_co_names | Washington """)

CATALOG.term('TX_co_names', r"""
    Anderson | Andrews | Angelina | Aransas | Archer | Armstrong | Atascosa
    | Austin | Bailey | Bandera | Bastrop | Baylor | Bee | Bell | Bexar
    | Blanco | Borden | Bosque | Bowie | Brazoria | Brazos | Brewster
    | Briscoe | Brooks | Brown | Burleson | Burnet | Caldwell | Calhoun
    | Callahan | Cameron | Camp | Carson | Cass | Castro | Chambers | Cherokee
    | Childress | Clay | Cochran | Coke | Coleman | Collin | Collingsworth
    | Comal | Comanche | Concho | Cooke | Coryell | Cottle | Crane
    | Crockett | Crosby | Culberson | Dallam | Dallas | Dawson | Deaf \s? Smith
    | Delta | Denton | DeWitt | Dickens | Dimmit | Donley | Duval | Eastland
    | Ector | Edwards | Ellis | El \s? Paso | Erath | Falls | Fannin | Fayette
    | Fisher | Floyd | Foard | Fort \s? Bend | Franklin | Freestone | Frio
    | Gaines | Galveston | Garza | Gillespie | Glasscock | Goliad | Gonzales
    | Gray | Grayson | Gregg | Grimes | Guadalupe | Hale | Hall | Hamilton
    | Hansford | Hardeman | Hardin | Harris | Harrison | Hartley | Haskell
    | Hays | Hemphill | Henderson | Hidalgo | Hill | Hockley | Hood | Hopkins
    | Houston | Howard | Hudspeth | Hunt | Hutchinson | Irion | Jack | Jackson
    | Jasper | Jeff \s? Davis | Jefferson | Jim \s? Hogg | Jim \s? Wells
    | Johnson | Jones | Karnes | Kaufman | Kendall | Kenedy | Kent | Kerr
    | Kimble | King | Kinney | Kleberg | Knox | Lamar | Lamb | Lampasas
    | La \s? Salle | Lavaca | Lee | Leon | Liberty | Limestone | Lipscomb
    | Live \s? Oak | Llano | Loving | Lubbock | Lynn | McCulloch | McLennan
    | McMullen | Madison | Marion | Martin | Mason | Matagorda | Maverick
    | Medina | Menard | Midland | Milam | Mills | Mitchell | Montague
    | Montgomery | Moore | Morris | Motley | Nacogdoches | Navarro | Newton
    | Nolan | Nueces | Ochiltree | Oldham | Orange | Palo \s? Pinto | Panola
    | Parker | Parmer | Pecos | Polk | Potter | Presidio | Rains | Randall
    | Reagan | Real | Red \s? River | Reeves | Refugio | Roberts | Robertson
    | Rockwall | Runnels | Rusk | Sabine | San \s? Augustine | San \s? Jacinto
    | San \s? Patricio | San \s? Saba | Schleicher | Scurry | Shackelford
    | Shelby | Sherman | Smith | Somervell | Starr | Stephens | Sterling
    | Stonewall | Sutton | Swisher | Tarrant | Taylor | Terrell | Terry
    | Throckmorton | Titus | Tom \s? Green | Travis | Trinity | Tyler
    | Upshur | Upton | Uvalde | Val \s? Verde | Van \s? Zandt | Victoria
    | Walker | Waller | Ward | Webb | Wharton | Wheeler | Wichita
    | Wilbarger | Willacy | Williamson | Wilson | Winkler | Wise | Wood
    | Yoakum | Young | Zapata | Zavala """)
CATALOG.grouper('TX_co', """ TX_co_names | Colorado | Washington """)

CATALOG.term('UM_co_names', r"""
    Baker ( \s Island )? | Howland ( \s Island )? | Jarvis ( \s Island )?
    | Johnston \s? Atoll | Kingman \s? Reef | Midway \s? Atoll
    | Navassa ( \s Island )? | Palmyra \s? Atoll | Wake ( \s Island )? """)
CATALOG.grouper('UM_co', """ UM_co_names """)

CATALOG.term('UT_co_names', r"""
    Beaver | Box \s? Elder | Cache | Carbon | Daggett | Davis | Duchesne
    | Emery | Garfield | Grand | Iron | Juab | Kane | Millard | Morgan | Piute
    | Rich | Salt \s? Lake | San \s? Juan | Sanpete | Sevier | Summit | Tooele
    | Uintah | Wasatch | Wayne | Weber """)
CATALOG.grouper('UT_co', """ UT_co_names | Utah | Washington """)

CATALOG.term('VT_co_names', r"""
    Addison | Bennington | Caledonia | Chittenden | Essex | Franklin
    | Grand \s? Isle | Lamoille | Orange | Orleans | Rutland | Windham
    | Windsor """)
CATALOG.grouper('VT_co', """ VT_co_names | Washington """)

CATALOG.term('VI_co_names', r"""
    Saint \s? Croix ( \s Island )? | Saint \s? John ( \s Island )?
    | Saint \s? Thomas ( \s Island )? """)
CATALOG.grouper('VI_co', """ VI_co_names """)

CATALOG.term('VA_co_names', r"""
    Accomack | Albemarle | Alleghany | Amelia | Amherst | Appomattox
    | Arlington | Augusta | Bath | Bedford | Bland | Botetourt | Brunswick
    | Buchanan | Buckingham | Campbell | Caroline | Carroll | Charles \s? City
    | Charlotte | Chesterfield | Clarke | Craig | Culpeper | Cumberland
    | Dickenson | Dinwiddie | Essex | Fairfax | Fauquier | Floyd | Fluvanna
    | Franklin | Frederick | Giles | Gloucester | Goochland | Grayson | Greene
    | Greensville | Halifax | Hanover | Henrico | Henry | Highland
    | Isle \s? of \s? Wight | James \s? City | King \s? and \s? Queen
    | King \s? George | King \s? William | Lancaster | Lee | Loudoun | Louisa
    | Lunenburg | Madison | Mathews | Mecklenburg | Middlesex | Montgomery
    | Nelson | New \s? Kent | Northampton | Northumberland | Nottoway | Orange
    | Page | Patrick | Pittsylvania | Powhatan | Prince \s? Edward
    | Prince \s? George | Prince \s? William | Pulaski | Rappahannock
    | Richmond | Roanoke | Rockbridge | Rockingham | Russell | Scott
    | Shenandoah | Smyth | Southampton | Spotsylvania | Stafford | Surry
    | Sussex | Tazewell | Warren | Westmoreland | Wise | Wythe
    | York | Alexandria | Bristol | Buena \s? Vista | Charlottesville
    | Chesapeake | Colonial \s? Heights | Covington | Danville | Emporia
    | Fairfax | Falls \s? Church | Franklin | Fredericksburg | Galax | Hampton
    | Harrisonburg | Hopewell | Lexington | Lynchburg | Manassas
    | Manassas \s? Park | Martinsville | Newport \s? News | Norfolk | Norton
    | Petersburg | Poquoson | Portsmouth | Radford | Richmond | Roanoke | Salem
    | Staunton | Suffolk | Virginia \s? Beach | Waynesboro | Williamsburg
    | Winchester """)
CATALOG.grouper('VA_co', """ VA_co_names | Washington """)

CATALOG.term('WA_co_names', r"""
    Adams | Asotin | Benton | Chelan | Clallam | Clark | Columbia | Cowlitz
    | Douglas | Ferry | Franklin | Garfield | Grant | Grays \s? Harbor | Island
    | Jefferson | King | Kitsap | Kittitas | Klickitat | Lewis | Lincoln
    | Mason | Okanogan | Pacific | Pend \s? Oreille | Pierce | San \s? Juan
    | Skagit | Skamania | Snohomish | Spokane | Stevens | Thurston | Wahkiakum
    | Walla \s? Walla | Whatcom | Whitman | Yakima """)
CATALOG.grouper('WA_co', """ WA_co_names """)

CATALOG.term('WV_co_names', r"""
    Barbour | Berkeley | Boone | Braxton | Brooke | Cabell | Calhoun | Clay
    | Doddridge | Fayette | Gilmer | Grant | Greenbrier | Hampshire | Hancock
    | Hardy | Harrison | Jackson | Jefferson | Kanawha | Lewis | Lincoln
    | Logan | McDowell | Marion | Marshall | Mason | Mercer | Mineral | Mingo
    | Monongalia | Monroe | Morgan | Nicholas | Pendleton | Pleasants
    | Pocahontas | Preston | Putnam | Raleigh | Randolph | Ritchie | Roane
    | Summers | Taylor | Tucker | Tyler | Upshur | Wayne | Webster | Wetzel
    | Wirt | Wood """)
CATALOG.grouper('WV_co', """ WV_co_names | Ohio | Wyoming """)

CATALOG.term('WI_co_names', r"""
    Adams | Ashland | Barron | Bayfield | Brown | Buffalo | Burnett | Calumet
    | Chippewa | Clark | Columbia | Crawford | Dane | Dodge | Door | Douglas
    | Dunn | Eau \s? Claire | Florence | Fond \s? du \s? Lac | Forest | Grant
    | Green | Green \s? Lake | Iron | Jackson | Jefferson | Juneau
    | Kenosha | Kewaunee | La \s? Crosse | Lafayette | Langlade | Lincoln
    | Manitowoc | Marathon | Marinette | Marquette | Menominee | Milwaukee
    | Monroe | Oconto | Oneida | Outagamie | Ozaukee | Pepin | Pierce | Polk
    | Portage | Price | Racine | Richland | Rock | Rusk | St\.? \s? Croix
    | Sauk | Sawyer | Shawano | Sheboygan | Taylor | Trempealeau | Vernon
    | Vilas | Walworth | Washburn | Waukesha | Waupaca | Waushara
    | Winnebago | Wood """)
CATALOG.grouper('WI_co', """ WI_co_names | Iowa | Washington """)

CATALOG.term('WY_co_names', r"""
    Albany | Big \s? Horn | Campbell | Carbon | Converse | Crook | Fremont
    | Goshen | Hot \s? Springs | Johnson | Laramie | Lincoln | Natrona
    | Niobrara | Park | Platte | Sheridan | Sublette | Sweetwater | Teton
    | Uinta | Washakie | Weston """)
CATALOG.grouper('WY_co', """ WY_co_names """)


CATALOG.grouper('us_county', """
    AL_co AK_co AZ_co AR_co CA_co CO_co CT_co DE_co DC_co FL_co GA_co HI_co
    ID_co IL_co IN_co IA_co KS_co KY_co LA_co ME_co MD_co MA_co MI_co MN_co
    MS_co MO_co MT_co NE_co NV_co NH_co NJ_co NM_co NY_co NC_co ND_co OH_co
    OK_co OR_co PA_co RI_co SC_co SD_co TN_co TX_co UT_co VT_co VA_co WA_co
    WV_co WI_co WY_co AS_co GU_co MP_co PR_co VI_co UM_co """.split())
