import json
import sys
# track list
track_list = [
    "barcelona",
    "barcelona_2019",
    "brands_hatch",
    "brands_hatch_2019",
	"kyalami_2019",
	"laguna_seca_2019",
    "hungaroring",
    "hungaroring_2019",
    "misano",
    "misano_2019",
    "monza",
    "monza_2019",
	"mount_panorama_2019",
    "nurburgring",
    "nurburgring_2019",
    "paul_ricard",
    "paul_ricard_2019",
    "silverstone",
    "silverstone_2019",
    "spa",
    "spa_2019",
	"suzuka_2019",
    "zolder",
    "zolder_2019",
    "zandvoort",
    "zandvoort_2019",
]

def main(track_name):
    track_name = track_name.lower()
    if track_name not in track_list:
        print("%s not found" % (track_name))
        sys.exit(1)
    print("Reading config")
    event = json.load(open("serverConfigs/event.json", "r"))
    event['track'] = track_name
    with open('serverConfigs/event.json', 'w', encoding='utf-8') as f:
        json.dump(event, f, ensure_ascii=False, indent=4)
    print("Written track to new folder")

if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv
    if len(args) == 2:
        main(args[1])
    else:
        print("Not enough args given")