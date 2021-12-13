# -*- coding: utf-8 -*-
{
    "name": "Custom Fields for Contacts",
    "version": "12.0.1.0.1",
    "category": "Extra Tools",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/12.0/custom-fields-for-contacts-342",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "contacts",
        "custom_fields"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/custom_partner_field.xml",
        "views/partner_custom_type.xml",
        "views/res_partner.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to add new fields for Odoo contacts without any technical knowledge",
    "description": """
    Often Odoo contacts' fields are not enough to reflect specifics of your relations with partners, while customization requires developer competences. This tool is introduced to make everything as simple as creating a new document in Odoo. The app let you prepare new partner properties fast and comfortable.

    Fields creation without technical knowledge
    Simple interface placement
    Contact complementary typology
    Partner custom fields
    Partner form with custom fields
    Custom fields: multiple types to select
    Different fields for different contact types
    Custom fields: drop-down choice
    Partner custom fields' menu
    I faced the error: QWeb2: Template 'X' not found
    <div class="knowsystem_block_title_text">
            <div class="knowsystem_snippet_general" style="margin:0px auto 0px auto;width:100%;">
                <table align="center" cellspacing="0" cellpadding="0" border="0" class="knowsystem_table_styles" style="width:100%;background-color:transparent;border-collapse:separate;">
                    <tbody>
                        <tr>
                            <td width="100%" class="knowsystem_h_padding knowsystem_v_padding o_knowsystem_no_colorpicker" style="padding:20px;vertical-align:top;text-align:inherit;">
                                
                                <ol style="margin:0px 0 10px 0;list-style-type:decimal;"><li><p class="" style="margin:0px;">Restart your Odoo server and update the module</p></li><li><p class="" style="margin:0px;">Clean your browser cashe (Ctrl + Shift + R) or open Odoo in a private window.</p></li></ol></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    What are update policies of your tools?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 115% }
	</style>


</p><p lang="en-US" style="margin:0px 0px 0.25cm 0px;line-height:120%;">According to the current Odoo Apps Store policies:</p><ul style="margin:0px 0 10px 0;list-style-type:disc;"><li><p lang="en-US" style="margin:0px;line-height:120%;"> every module bought for the version 12.0 and prior gives you an access to the all versions up to 12.0. </p></li><li><p lang="en-US" style="margin:0px;line-height:120%;">starting from the version 13.0, every version of the module should be purchased separately.</p></li><li><p lang="en-US" style="margin:0px;line-height:120%;">disregarding the version, purchasing a tool grants you a right for all updates and bug fixes within a major version.<br></p></li></ul><p lang="en-US" style="margin:0px 0px 0.25cm 0px;line-height:120%;">Take into account that Odoo Tools team does not control those policies. By all questions please contact the Odoo Apps Store representatives <a href="https://www.odoo.com/contactus" style="text-decoration:none;color:rgb(13, 103, 89);background-color:transparent;">directly</a>.</p>
    May I buy your app from your company directly?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 10px 0px;">Sorry, but no. We distribute the
tools only through the <a href="https://apps.odoo.com/apps" style="text-decoration:none;color:rgb(13, 103, 89);background-color:transparent;">official Odoo apps store</a></p>
    How should I install your app?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="line-height:120%;margin:0px 0px 10px 0px;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><ol style="margin:0px 0 10px 0;list-style-type:decimal;">
	<li><p style="margin:0px;line-height:120%;">Unzip source code of purchased tools in one of your Odoo
	add-ons directory</p>
	</li><li><p style="margin:0px;line-height:120%;">Re-start the Odoo server</p>
	</li><li><p style="margin:0px;line-height:120%;">Turn on the developer mode (technical settings)</p>
	</li><li><p style="margin:0px;line-height:120%;">Update the apps' list (the apps' menu)</p>
	</li><li><p style="margin:0px;line-height:120%;">Find the app and push the button 'Install'</p>
	</li><li><p style="margin:0px;line-height:120%;">Follow the guidelines on the app's page if those exist.</p>
</li></ol>
    Your tool has dependencies on other app(s). Should I purchase those?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, all modules marked in dependencies are absolutely required for a correct work of our tool. Take into account that price marked on the app page already includes all necessary dependencies.&nbsp;&nbsp;</p>
    I noticed that your app has extra add-ons. May I purchase them afterwards?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, sure. Take into account that Odoo
automatically adds all dependencies to a cart. You should exclude
previously purchased tools.</p>
    I would like to get a discount
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Regretfully, we do not have a
technical possibility to provide individual prices.</p>
    How can I install your app on Odoo.sh?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 10px 0px;">As soon as you purchased the
app, the button 'Deploy on Odoo.sh' will appear on the app's page in
the Odoo store. Push this button and follow the instructions.</p>
<p style="margin:0px 0px 10px 0px;">Take into account that for paid
tools you need to have a private GIT repository linked to your
Odoo.sh projects</p>
    May I install the app on my Odoo Online (SaaS) database?
    <p style="margin:0px 0px 10px 0px;">No, third party apps can not be used on Odoo Online.</p>
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "10.0",
    "currency": "EUR",
}