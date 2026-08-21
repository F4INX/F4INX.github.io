---
layout: post
title: Export QGIS maps and terrain height data to Forsk Atoll.
permalink: /posts/QGIS-to-Atoll.html
last_modified_at: 2023-10-09 12:17
categories: [Software, QGIS, Tools]
---

Forsk Atoll antenna planning software is not so hard to use when a suitable map and terrain height data is available for import into Atoll. However such ready to use data is rather hard to find and finding such data is the top question asked in the comments of most Atoll tutorials.

Here is a tutorial to make a pretty convenient map with QGIS, usefull for all needs besides just Atoll, and to export relevant data towards Atoll.

## QGIS

### Installation

Install QGIS uing the OSGeo4W bundle. Ensure the following is checked for install:

* QGIS
* matplotlib
* numpy

If you see the following or similar error message, check the installed packages in OSGeo4W.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-01-missing-modules.png' | relative_url }}">

### Map and height map preparation

The steps of this part are long, but thanksfully must be done only once and can be reused for several projects. A starting file is given here: [QGIS-base.qgz]({{ '/posts/QGIS-to-Atoll/QGIS-base.qgz' | relative_url }}). When using this file, skip straight until [Bookmark needed area](#bookmark-needed-area).

#### Coordinate reference system

Project -> New (Ctrl + N)

Project -> Properties

Select the WGS 84 / UTM zone corresponding to the area of the study. For France, its UTM 31N (EPSG 32631). Antenna coverage studies are usually on a scale sufficiently small to make UTM practical, and the distances coordinates makes life much easier when estimating distances, for instance for antenna simulation radius settings.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-02-CRS-selection.png' | relative_url }}">

#### OpenStreetMaps and transparency

By default, the OpenStreetMaps vector layers are opaque. Configuration is needed in order to make it transparent to overlay it on satellite imagery.

##### Short way

Import this layer file with all the settings: [openstreetmap-vector-overlay.qlr]({{ '/posts/QGIS-to-Atoll/openstreetmap-vector-overlay.qlr' | relative_url }}) and skip next section.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-03-import-layer.png' | relative_url }}">

##### Long way

In case for whatever reason you want to do the previous step manually, here are the instructions. In most case, you ought better import the settings as shown in previous section.

Add OSM map using Vector Tiles -> OpenStreetMap vector:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-04-OpenStreetMaps.png' | relative_url }}">

Using QuickMapServices plugin, add satellite picture using QuickMap Services -> ESRI -> ESRI Satellite. The satellite view is not immediately visible because the layer is added behind the previouly added one:
 
<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-05-satellite.png' | relative_url }}">

Go to OpenStreetMaps vector properties and :

Uncheck background:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-06-uncheck-background.png' | relative_url }}" width="75%">

Uncheck fills:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-07-uncheck-fills.png' | relative_url }}" width="75%">

Uncheck patterns:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-08-uncheck-pattern.png' | relative_url }}" width="75%">

Uncheck landcovers with exception of outlines:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-09-uncheck-landcover.png' | relative_url }}" width="75%">

Uncheck water areas with exception of outlines:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-10-uncheck-water-area.png' | relative_url }}" width="75%">

Uncheck transportation areas:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-11-uncheck-transportation-area.png' | relative_url }}" width="75%">

Uncheck oceans:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-12-uncheck-ocean.png' | relative_url }}" width="75%">

Uncheck leaf types:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-13-uncheck-leaf-type.png' | relative_url }}" width="75%">

Uncheck waterways :

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-14-uncheck-waterway.png' | relative_url }}" width="75%">

Recheck all outlines in case some outline were accidentally unchecked in previous steps:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-15-recheck-outline.png' | relative_url }}" width="75%">

#### Contour maps

Using the browser pane on left, add Maptiler Topo.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-16-MapTiler-Topo.png' | relative_url }}">

From Maptiler topo, keep only Contours, and place it between satellite layer and overlayed map.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-17-keep-contour.png' | relative_url }}">

Check again in project properties that project coordinate reference system is the wanted one.

#### Bookmark needed area

View the extent of the area you need, next go View -> New Spatial Bookmark… (Ctrl B):

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-18-bookmark.png' | relative_url }}">

#### Height map preparation

Double-click on bookmark to be sure the display canvas matches it. Download height maps using the SRTM downloader icon:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-19-SRTM-downloader-1.png' | relative_url }}">

Click set canvas extent, and put « ./ » in output path:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-20-SRTM-downloader-2.png' | relative_url }}" width="50%">

Usually, STRM downloader downloads only a single SRTM maps since their map cutting is quite big:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-21-SRTM-downloader-3.png' | relative_url }}" width="50%">

Here, KeePass and Ctrl+Alt+A can be quite useful.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-22-SRTM-downloader-4.png' | relative_url }}" width="50%">

After the layer being downloaded, you should see it. Reorder the layers to check it matches other layers:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-23-check-height-layer.png' | relative_url }}">

Next, uncheck the height layer but keep it:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-24-hide-height-layer.png' | relative_url }}">

### Map and height map export

#### Map export

Go to Project -> Export -> Export Map to Image:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-25-save-image-menu.png' | relative_url }}">

Select first the suitable scale and resolution (good values are 1:40000, 300 dpi) and next select your bookmark:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-26-save-image-settings.png' | relative_url }}" width="50%">

Save as JPG format, convenient because satellite images hard to compress in PNG.

#### Height map export

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-27-save-height-map-menu.png' | relative_url }}">

Settings :

* Select « Raw Data ».
* Select « Erdas Imagine Images(.img).
* Select CRS WRS 84 / UTM correct zone.
* Extent : select bookmarks.
* Resolution : round the best (lowest) value and use it for both horizontal and vertical because Atoll can’t handle different resolution on the axes.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-28-save-height-map-settings.png' | relative_url }}">

## Atoll

### Coordinate reference system

In your project, go do Document -> Properties…:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-29-document-properties.png' | relative_url }}">

Next, select WGS 84 / UTM correct zone for projection and display:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-30-coordinates.png' | relative_url }}">

### Map import

In Geo tab, create an Offline Maps folder for the created map:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-31-new-folder-1.png' | relative_url }}">

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-32-new-folder-2.png' | relative_url }}">

Import the map into Offline Maps:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-33-map-import-1.png' | relative_url }}">

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-34-map-import-2.png' | relative_url }}">

### Height map import

Next, import the height file:

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-35-height-import-1.png' | relative_url }}">

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-36-height-import-2.png' | relative_url }}">

Note both maps covers the same area of the QGIS bookmark.
Once the correctness of the height map import is checked, this layer can be hidden, still it will be correctly taken into accout for calculations.

## Atoll example

With map and height data generated by the previously described methods, the following **quick draft** of DVB-T digital television coverage simulation was performed on an area where reception is difficult. Transmitters positions come from ANFR Cartoradio[^1] and powers come from a forum [^2]<sup>,</sup>[^3]. Of course, this **quick draft** must be refined, particularly concerning the radiation diagrams of some antennas. Nevertheless, the reception hole in the Ennuyé valley around Bésignan can be seen immediately due to the blocade of the Ventoux transmitter by the south mountain. The others transmitters are not significant on a wide scale because their are low power district transmitters.

<img src="{{ '/posts/QGIS-to-Atoll/QGIS-to-Atoll-37-quick-try.jpg' | relative_url }}">

[^1]: [https://www.cartoradio.fr/](https://www.cartoradio.fr/)

[^2]: [http://www.tvnt.net/forum/26-drome-t12652.html](http://www.tvnt.net/forum/26-drome-t12652.html)

[^3]: [http://www.tvnt.net/forum/84-vaucluse-t12658.html](http://www.tvnt.net/forum/84-vaucluse-t12658.html)
