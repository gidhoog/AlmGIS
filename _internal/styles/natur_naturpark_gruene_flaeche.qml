<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="0" version="3.4.2-Madeira" simplifyDrawingTol="1" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" maxScale="0" simplifyDrawingHints="1" simplifyAlgorithm="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol name="0" type="fill" clip_to_extent="1" alpha="1">
        <layer enabled="1" pass="0" class="SimpleFill" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="154,182,137,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="129,152,115,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/0/id" value="transparency"/>
    <property key="embeddedWidgets/count" value="1"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory height="15" width="15" scaleBasedVisibility="0" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" lineSizeType="MM" minScaleDenominator="0" backgroundAlpha="255" rotationOffset="270" scaleDependency="Area" enabled="0" barWidth="5" opacity="1" backgroundColor="#ffffff" minimumSize="0" sizeType="MM" penColor="#000000" penWidth="0" penAlpha="255">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" priority="0" showAll="1" placement="1" obstacle="0" zIndex="0" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="OBJECTID">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="GID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="INTERNALID">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NAME">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LEGISLATIONTITLE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LEGISLATIONCODE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LEGALFOUNDATIONDATE">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="IUCN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="EXTERNALID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PGNAME_LIST">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PBNAME_LIST">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="EMASST">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LASTUPDATE">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="OBJECTID"/>
    <alias name="" index="1" field="GID"/>
    <alias name="" index="2" field="INTERNALID"/>
    <alias name="" index="3" field="NAME"/>
    <alias name="" index="4" field="LEGISLATIONTITLE"/>
    <alias name="" index="5" field="LEGISLATIONCODE"/>
    <alias name="" index="6" field="LEGALFOUNDATIONDATE"/>
    <alias name="" index="7" field="IUCN"/>
    <alias name="" index="8" field="EXTERNALID"/>
    <alias name="" index="9" field="PGNAME_LIST"/>
    <alias name="" index="10" field="PBNAME_LIST"/>
    <alias name="" index="11" field="EMASST"/>
    <alias name="" index="12" field="LASTUPDATE"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="OBJECTID" expression="" applyOnUpdate="0"/>
    <default field="GID" expression="" applyOnUpdate="0"/>
    <default field="INTERNALID" expression="" applyOnUpdate="0"/>
    <default field="NAME" expression="" applyOnUpdate="0"/>
    <default field="LEGISLATIONTITLE" expression="" applyOnUpdate="0"/>
    <default field="LEGISLATIONCODE" expression="" applyOnUpdate="0"/>
    <default field="LEGALFOUNDATIONDATE" expression="" applyOnUpdate="0"/>
    <default field="IUCN" expression="" applyOnUpdate="0"/>
    <default field="EXTERNALID" expression="" applyOnUpdate="0"/>
    <default field="PGNAME_LIST" expression="" applyOnUpdate="0"/>
    <default field="PBNAME_LIST" expression="" applyOnUpdate="0"/>
    <default field="EMASST" expression="" applyOnUpdate="0"/>
    <default field="LASTUPDATE" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="OBJECTID" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="GID" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="INTERNALID" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="NAME" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="LEGISLATIONTITLE" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="LEGISLATIONCODE" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="LEGALFOUNDATIONDATE" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="IUCN" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="EXTERNALID" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="PGNAME_LIST" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="PBNAME_LIST" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="EMASST" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="LASTUPDATE" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="OBJECTID"/>
    <constraint exp="" desc="" field="GID"/>
    <constraint exp="" desc="" field="INTERNALID"/>
    <constraint exp="" desc="" field="NAME"/>
    <constraint exp="" desc="" field="LEGISLATIONTITLE"/>
    <constraint exp="" desc="" field="LEGISLATIONCODE"/>
    <constraint exp="" desc="" field="LEGALFOUNDATIONDATE"/>
    <constraint exp="" desc="" field="IUCN"/>
    <constraint exp="" desc="" field="EXTERNALID"/>
    <constraint exp="" desc="" field="PGNAME_LIST"/>
    <constraint exp="" desc="" field="PBNAME_LIST"/>
    <constraint exp="" desc="" field="EMASST"/>
    <constraint exp="" desc="" field="LASTUPDATE"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="OBJECTID" type="field" hidden="0" width="-1"/>
      <column name="GID" type="field" hidden="0" width="-1"/>
      <column name="INTERNALID" type="field" hidden="0" width="-1"/>
      <column name="NAME" type="field" hidden="0" width="-1"/>
      <column name="LEGISLATIONTITLE" type="field" hidden="0" width="-1"/>
      <column name="LEGISLATIONCODE" type="field" hidden="0" width="-1"/>
      <column name="LEGALFOUNDATIONDATE" type="field" hidden="0" width="-1"/>
      <column name="IUCN" type="field" hidden="0" width="-1"/>
      <column name="EXTERNALID" type="field" hidden="0" width="-1"/>
      <column name="PGNAME_LIST" type="field" hidden="0" width="-1"/>
      <column name="PBNAME_LIST" type="field" hidden="0" width="-1"/>
      <column name="EMASST" type="field" hidden="0" width="-1"/>
      <column name="LASTUPDATE" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="EMASST" editable="1"/>
    <field name="EXTERNALID" editable="1"/>
    <field name="GID" editable="1"/>
    <field name="INTERNALID" editable="1"/>
    <field name="IUCN" editable="1"/>
    <field name="LASTUPDATE" editable="1"/>
    <field name="LEGALFOUNDATIONDATE" editable="1"/>
    <field name="LEGISLATIONCODE" editable="1"/>
    <field name="LEGISLATIONTITLE" editable="1"/>
    <field name="NAME" editable="1"/>
    <field name="OBJECTID" editable="1"/>
    <field name="PBNAME_LIST" editable="1"/>
    <field name="PGNAME_LIST" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="EMASST" labelOnTop="0"/>
    <field name="EXTERNALID" labelOnTop="0"/>
    <field name="GID" labelOnTop="0"/>
    <field name="INTERNALID" labelOnTop="0"/>
    <field name="IUCN" labelOnTop="0"/>
    <field name="LASTUPDATE" labelOnTop="0"/>
    <field name="LEGALFOUNDATIONDATE" labelOnTop="0"/>
    <field name="LEGISLATIONCODE" labelOnTop="0"/>
    <field name="LEGISLATIONTITLE" labelOnTop="0"/>
    <field name="NAME" labelOnTop="0"/>
    <field name="OBJECTID" labelOnTop="0"/>
    <field name="PBNAME_LIST" labelOnTop="0"/>
    <field name="PGNAME_LIST" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>OBJECTID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
