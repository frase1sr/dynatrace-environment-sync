# Dynatrace Environment Sync Script

DEPENDENCIES
<ul><li>Requests</li></ul>

CURRENT FEATURES
<ul><li>Sync between Master and secondary enviroment for</li>
	<ul>
	 <li>Request Attribute Rules</li>
	 <li>Automatically applied tag rules</li>
	 <li>Management Zones</li>
	</ul>
	</ul>
</br>
UPCOMING 
<ul><li>Sync between Master and secondary enviroment for</li>
	<ul>
	 <li>~Custom Services</li>
	</ul>
</ul>
HOW TO RUN
<ol>
	 <li>Install the python requests library </li>
	 <li>Change the configuration varibles at the top of the files.</li>
		<ul><li>masterEnv = "https://INSERT_ID.live.dynatrace.com/api/config/v1/" the environment path that you would like to copy the configurations FROM</li>
		<li>masterEnvToken =  "INSERT_TOKEN" the environment token that you would like to copy the configurations TO</li>
		<li>syncEnvs = ["https://INSERT_ID.live.dynatrace.com/api/config/v1/,"asdfas"] the environment path that you would like to copy the configurations from</li>
		<li>requestAttributesEnabled = "True" if you would like to sync the Request Attributes configurationv</li>   
		<li>autoTaggingRulesEnabled = "True" if you would like to sync the Automatically applied tags configurations</li>
		<li>managementZonesRulesEnabled = "True" if you would like to sync the Managment Zones confguration</li>
		<li>addNotExisting = "True" if you would like to add the rules that do not exist in your sync environment, but do in the Master environment</li>
		<li>updateExisting = "True" if you would like to update the current rules in the sync rules with the configuration from the Master environment</li></ul></ol>
Both of the above settings match on the NAME of the rules, so the rules must have the same name, otherwise it will match them
