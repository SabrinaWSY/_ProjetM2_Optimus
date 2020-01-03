<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="./stylesheet.css"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>

<!-- Structure generale de la page HTML -->
<xsl:template match="/">
<html>
	<head>
		<title><xsl:value-of select="//INFO/AUTEUR"/><xsl:value-of select="//INFO/FORMATION"/> </title>
		<meta http-equiv="Content-Type" content="text/html" charset="UTF-8"/>
		<script type="text/javascript" src="js/jquery-1.4.2.min.js"></script>
		<script type="text/javascript" src="js/slimbox2.js"></script>
		<script type="text/javascript" src="js/message.js"></script>
		<link rel="stylesheet" type="text/css" href="stylesheet.css"/>
	</head>

	<body>

	<div id="wrap">
		<!-- Partie droite -->
		<div id="right">

			<div id="header">
				<h1><xsl:value-of select="//INFO/TITRE"/></h1>
				<h4><xsl:value-of select="//INFO/FORMATION"/></h4>
				<h4><xsl:value-of select="//INFO/AUTEUR"/></h4>
			</div>



			<div id="contenu">
				<xsl:apply-templates select="//DOC/CONTENU"/>
			</div>

			<div id="footer">
				<br />
				Master 2 TAL Ingénierie Multilingue - Siyu WANG, Shuai GAO et Chen SUN - Année 2019/2020
			</div>
		</div>
		<!-- Partie gauche (menu flottant vertical) -->
		<div id="left">
			<div id="menub">
				<ul>


				<li><a href="./index.xml">Accueil</a></li>
				<li><a href="./presentation.xml">Présentation</a></li>
				<li><a href="html/resultat.html">Résultats</a></li>
				
				<li><a href="#wrap">[Retour haut de page]</a></li>

				<xsl:if test='//DOC[@nom!="Accueil"]'>
				<xsl:for-each select=".//DIV[@id]">
				<a href="#{@id}"><xsl:value-of select="@titre"/></a>
				</xsl:for-each>
				</xsl:if>
				</ul>
			</div>
		</div>
	</div>
	
	</body>
	
</html>
</xsl:template>


<!-- Templates pour la selection et le formatage du contenu de chaque page xml -->

<!-- Pour les documents de type "page" -->
<xsl:template match='DOC[@type="page"]/CONTENU'>
	<xsl:for-each select='ART'>
		<div class="table">
			<xsl:if test='@entete'>
				<h2><xsl:value-of select="@entete"/></h2>
			</xsl:if>
			<xsl:if test='@titre'>
				<h2 id="{@nom}"><xsl:value-of select="@titre"/></h2>
			</xsl:if>
			<xsl:if test='@nom="about"'>
				<p>Nous sommes trois étudiants en deuxième année de Master TAL filière IM à Inalco :</p>
				<p><a href="mailto:sabrina.wang.siyu@gmail.com">Siyu WANG</a></p>
				<p><a href="mailto:gustavosturmgeist@hotmail.com">Shuai GAO</a></p>
				<p><a href="mailto:sonshin33@gmail.com">Chen SUN</a></p>
				
				<br />
			</xsl:if>
			<xsl:apply-templates select="."/>
		</div>
	</xsl:for-each>
</xsl:template>

<xsl:template match='DIV'>
	<span class="sstitre">
	<xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
	<xsl:value-of select="@titre"/>
	</span>
	<xsl:apply-templates/>
</xsl:template>

<!-- Eléments communs -->
<xsl:template match="TEXTE">
<span class="texte"><xsl:apply-templates/></span>
<br /><br />
</xsl:template>

<xsl:template match='TEXTE//LIEN|ART//LIEN'>
<a href="{@url}" target="_blank"><xsl:value-of select="."/></a>
</xsl:template>

<xsl:template match="CODE">
	<xsl:choose>
		<xsl:when test='starts-with(text(),"@")'>
			<span class="code" style='color:red;'><xsl:apply-templates/></span>
		</xsl:when>
		<xsl:when test="starts-with(text(),'&#34;')">
			<span class="code" style="color:#FFFFFF;"><xsl:apply-templates/></span>
		</xsl:when>
		<xsl:when test='starts-with(text(),"&#39;")'>
			<span class="code" style="color:#FFFFFF;"><xsl:apply-templates/></span>
		</xsl:when>
		<xsl:when test='contains(text(),"&lt;")'>
			<span class="code" style='color:blue;'><xsl:apply-templates/></span>
		</xsl:when>
		<xsl:otherwise>
			<span class="code" style='color:#FFFFFF;'><xsl:apply-templates/></span>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- Eléments de style HTML (pouvant être appliqués à tous les documents) -->
<xsl:template match='U'>
	<u><xsl:apply-templates/></u>
</xsl:template>

<xsl:template match='S'>
	<s><xsl:apply-templates/></s>
</xsl:template>

<xsl:template match='B'>
	<b><xsl:apply-templates/></b>
</xsl:template>

<xsl:template match='I'>
	<i><xsl:apply-templates/></i>
</xsl:template>

<xsl:template match="*[@color]">
<font color="{@color}"><xsl:apply-templates/></font>
</xsl:template>

<xsl:template match="LI">
<li><xsl:apply-templates/></li>
</xsl:template>

</xsl:stylesheet>