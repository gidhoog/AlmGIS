<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.2-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="20000" maxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>0</Searchable>
  </flags>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/0/id" value="transparency"/>
    <property key="embeddedWidgets/count" value="1"/>
    <property key="identify/format" value="Text"/>
  </customproperties>
  <pipe>
    <rasterrenderer opacity="1" band="1" alphaBand="-1" type="singlebandcolordata">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
    </rasterrenderer>
    <brightnesscontrast contrast="10" brightness="30"/>
    <huesaturation colorizeGreen="128" colorizeBlue="128" colorizeOn="0" colorizeStrength="100" grayscaleMode="0" saturation="20" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
