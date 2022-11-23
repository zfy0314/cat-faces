import json
import os
from collections import namedtuple

import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

Participant = namedtuple(
    "Participant", ["hash", "background", "pets", "criticals", "reals", "unrelateds"]
)

participants = []
for file_name in os.listdir("./results"):
    try:
        survey = json.load(open(os.path.join("surveys", file_name), "r"))
    except json.decoder.JSONDecodeError:
        print(file_name)
        continue
    result = {}
    for response in json.load(open(os.path.join("results", file_name), "r")):
        result.update(response)
    try:
        participants.append(
            Participant(
                hash=file_name[:-5],
                background=survey["cog_background"],
                pets=survey["pet_cat"],
                criticals=[
                    int(result["critical1-recall"]),
                    int(result["critical2-recall"]),
                ],
                reals=[int(result["cat1-recall"]), int(result["cat2-recall"])],
                unrelateds=[
                    int(result["unrelated1-recall"]),
                    int(result["unrelated2-recall"]),
                ],
            )
        )
    except KeyError:
        print(file_name)

real_overall = sum([P.reals for P in participants], [])
critical_overall = sum([P.criticals for P in participants], [])
unrelated_overall = sum([P.unrelateds for P in participants], [])

real_cog = sum([P.reals for P in participants if P.background != "none"], [])
critical_cog = sum([P.criticals for P in participants if P.background != "none"], [])
unrelated_cog = sum([P.unrelateds for P in participants if P.background != "none"], [])
real_nocog = sum([P.reals for P in participants if P.background == "none"], [])
critical_nocog = sum([P.criticals for P in participants if P.background == "none"], [])
unrelated_nocog = sum(
    [P.unrelateds for P in participants if P.background == "none"], []
)

real_cat = sum([P.reals for P in participants if P.pets != "none"], [])
critical_cat = sum([P.criticals for P in participants if P.pets != "none"], [])
unrelated_cat = sum([P.unrelateds for P in participants if P.pets != "none"], [])
real_nocat = sum([P.reals for P in participants if P.pets == "none"], [])
critical_nocat = sum([P.criticals for P in participants if P.pets == "none"], [])
unrelated_nocat = sum([P.unrelateds for P in participants if P.pets == "none"], [])

colors = ["pink", "lightblue", "lightgreen"]
annotate = (
    lambda x: "***"
    if x.pvalue < 0.001
    else "**"
    if x.pvalue < 0.01
    else "*"
    if x.pvalue < 0.05
    else "n.s."
)

boxplot = plt.boxplot(
    [real_overall, critical_overall, unrelated_overall],
    labels=["studied", "critical lure", "unrelated lure"],
    patch_artist=True,
)
fig = plt.gcf()
fig.set_size_inches(8, 4.8)
for patch, color in zip(boxplot["boxes"], colors):
    patch.set_facecolor(color)
plt.ylim(0, 6)
plt.yticks(
    range(1, 5),
    [
        "pretty sure \n NOT studies",
        "kind of sure \n NOT studied",
        "kind of sure \n studied",
        "pretty sure \n studied",
    ],
)
plt.plot([1, 1, 1.95, 1.95], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(1.4, 4.7, annotate(ttest_ind(real_overall, critical_overall)))
plt.plot([2.05, 2.05, 3, 3], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(2.5, 4.7, annotate(ttest_ind(critical_overall, unrelated_overall)))
plt.plot([1, 1, 3, 3], [4.9, 5, 5, 4.9], color="black")
plt.text(1.95, 5.1, annotate(ttest_ind(real_overall, unrelated_overall)))
plt.title("overall (n = 32)")
plt.savefig("overall.jpg")
plt.close()


boxplot = plt.boxplot(
    [
        real_cog,
        critical_cog,
        unrelated_cog,
        real_nocog,
        critical_nocog,
        unrelated_nocog,
    ],
    labels=[
        "studied",
        "critical lure",
        "unrelated lure",
        "studied",
        "critical lure",
        "unrelated lure",
    ],
    patch_artist=True,
)
fig = plt.gcf()
fig.set_size_inches(12.8, 6.4)
for patch, color in zip(boxplot["boxes"], colors + colors):
    patch.set_facecolor(color)
plt.ylim(0, 7.2)
plt.yticks(
    range(1, 5),
    [
        "pretty sure \n NOT studies",
        "kind of sure \n NOT studied",
        "kind of sure \n studied",
        "pretty sure \n studied",
    ],
)
plt.xlabel(
    " " * 0
    + "some cognitive science background (n=22)"
    + " " * 48
    + "no cognitive science background (n=10)"
    + " " * 4
)
plt.title("split by cognitive science background")
plt.plot([1, 1, 1.95, 1.95], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(1.4, 4.7, annotate(ttest_ind(real_cog, critical_cog)))
plt.plot([2.05, 2.05, 3, 3], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(2.5, 4.7, annotate(ttest_ind(critical_cog, unrelated_cog)))
plt.plot([1, 1, 3, 3], [4.9, 5, 5, 4.9], color="black")
plt.text(1.95, 5.1, annotate(ttest_ind(real_cog, unrelated_cog)))
plt.plot([4, 4, 4.95, 4.95], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(4.4, 4.7, annotate(ttest_ind(real_nocog, critical_nocog)))
plt.plot([5.05, 5.05, 6, 6], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(5.5, 4.7, annotate(ttest_ind(critical_nocog, unrelated_nocog)))
plt.plot([4, 4, 6, 6], [4.9, 5, 5, 4.9], color="black")
plt.text(4.95, 5.1, annotate(ttest_ind(real_nocog, unrelated_nocog)))
plt.plot([1, 1, 4, 4], [5.4, 5.5, 5.5, 5.4], color="black")
plt.text(2.45, 5.6, annotate(ttest_ind(real_cog, real_nocog)))
plt.plot([2, 2, 5, 5], [5.8, 5.9, 5.9, 5.8], color="black")
plt.text(3.45, 6.0, annotate(ttest_ind(critical_cog, critical_nocog)))
plt.plot([3, 3, 6, 6], [6.2, 6.3, 6.3, 6.2], color="black")
plt.text(4.45, 6.4, annotate(ttest_ind(unrelated_cog, unrelated_nocog)))
plt.savefig("cog.jpg")
plt.close()


boxplot = plt.boxplot(
    [
        real_cog,
        critical_cog,
        unrelated_cog,
        real_nocog,
        critical_nocog,
        unrelated_nocog,
    ],
    labels=[
        "studied",
        "critical lure",
        "unrelated lure",
        "studied",
        "critical lure",
        "unrelated lure",
    ],
    patch_artist=True,
)
fig = plt.gcf()
fig.set_size_inches(12.8, 6.4)
for patch, color in zip(boxplot["boxes"], colors + colors):
    patch.set_facecolor(color)
plt.ylim(0, 7.2)
plt.yticks(
    range(1, 5),
    [
        "pretty sure \n NOT studies",
        "kind of sure \n NOT studied",
        "kind of sure \n studied",
        "pretty sure \n studied",
    ],
)
plt.xlabel(
    " " * 0
    + "owns a pet at some point (n=16)"
    + " " * 68
    + "never a pet owner (n=16)"
    + " " * 6
)
plt.title("split by pet owner")
plt.plot([1, 1, 1.95, 1.95], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(1.4, 4.7, annotate(ttest_ind(real_cat, critical_cat)))
plt.plot([2.05, 2.05, 3, 3], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(2.5, 4.7, annotate(ttest_ind(critical_cat, unrelated_cat)))
plt.plot([1, 1, 3, 3], [4.9, 5, 5, 4.9], color="black")
plt.text(1.95, 5.1, annotate(ttest_ind(real_cat, unrelated_cat)))
plt.plot([4, 4, 4.95, 4.95], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(4.4, 4.7, annotate(ttest_ind(real_nocat, critical_nocat)))
plt.plot([5.05, 5.05, 6, 6], [4.5, 4.6, 4.6, 4.5], color="black")
plt.text(5.45, 4.7, annotate(ttest_ind(critical_nocat, unrelated_nocat)))
plt.plot([4, 4, 6, 6], [4.9, 5, 5, 4.9], color="black")
plt.text(4.95, 5.1, annotate(ttest_ind(real_nocat, unrelated_nocat)))
plt.plot([1, 1, 4, 4], [5.4, 5.5, 5.5, 5.4], color="black")
plt.text(2.45, 5.6, annotate(ttest_ind(real_cat, real_nocat)))
plt.plot([2, 2, 5, 5], [5.8, 5.9, 5.9, 5.8], color="black")
plt.text(3.45, 6.0, annotate(ttest_ind(critical_cat, critical_nocat)))
plt.plot([3, 3, 6, 6], [6.2, 6.3, 6.3, 6.2], color="black")
plt.text(4.45, 6.4, annotate(ttest_ind(unrelated_cat, unrelated_nocat)))
print(len(unrelated_nocat))
plt.savefig("pet.jpg")
plt.close()
