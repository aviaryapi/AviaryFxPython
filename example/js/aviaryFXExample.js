
var uploadedFile;
var selectedEffect;
var renderOptionParamsArray = new Array();
var backgroundPosition = 	[
								"0px 0px", 		"-128px 0px", 		"-256px 0px",
								"0px -128px", 	"-128px -128px",	"-256px -128px",
								"0px -256px",	"-128px -256px",	"-256px -256px"
							];
var filters = new Array();

$(document).ready(function(){
	
	getFilters();
	
	$("#submit").click(function(){
		return ajaxFileUpload();
	});
	
	$(".selectEffect").change(function() {
		$(".selectEffect option:selected").each(function() {
			selectedEffect = $(this).val();
		});
		return renderOptions(selectedEffect, uploadedFile);
	});
	
});

/*
 * Get filters
 */
function getFilters()
{
	$.ajax({
		type: 'POST',
		url: 'cgi-bin/AviaryFxExample.py?q=getFilters',
		contentType: 'application/x-www-form-urlencoded',
		dataType: 'json',
		success: function(data, status)
		{
			$.each(data, function(i, item){
				var filter = new Object();
				filter["label"] = item.label;
				filter["uid"] = item.uid;
				filters.push(filter);
			});
			for(var i = 0; i < filters.length; i++) {
				$(".selectEffect").append('<option value="' + filters[i]["uid"] + '">' + filters[i]["label"] + '</option>');
			}
		},
		error: function(data, status, e)
		{
			alert(e);
		}
	});
	return false;
}

/*
 * Upload image
 * http://www.phpletter.com/Demo/AjaxFileUpload-Demo/
 */
function ajaxFileUpload() 
{
	$("#loading")
	.ajaxStart(function(){
		$(this).show();
		showLoader();
	})
	.ajaxComplete(function(){
		$ = jQuery.noConflict();
		$(this).hide();
		hideLoader();
		hideUploadForm();
		showEffectOptions();
	});

	$.ajaxFileUpload
	(
		{
			url:'cgi-bin/AviaryFxExample.py?q=upload',
			secureuri:false,
			fileElementId:'file',
			dataType: 'json',
			success: function (data, status)
			{
				var img = new Image();
				img.src = data.url;
				img.onload = function() {
					$("#imageArea").attr({ src: img.src });
					$.getScript("js/imagepanner.js");
				}
				uploadedFile = data.url;
				
				//alert(data.url);
			},
			error: function (data, status, e)
			{
				alert(e);
			}
		}
	)
	return false;
}

/*
 * Get render options
 */
function renderOptions(selectedEffect, uploadedFile) 
{
	$.ajax({
		type: 'POST',
		url: 'cgi-bin/AviaryFxExample.py?q=renderOptions',
		data: ({ filterid: selectedEffect, filepath: uploadedFile }),
		dataType: 'json',
		success: function(data, status)
		{
			var renderOptionsGrid = data.renderOptionsGrid;
			var renderOptionsImage = "url(" + renderOptionsGrid + ")";
			renderOptionParamsArray = [];
			$.each(data.renderOptionParams, function(i, item){
				//alert(item.parameters);
				renderOptionParamsArray[i] = item;
				console.log(renderOptionParamsArray[i]); 
			});
			
			$("#thumbs div").remove();
			
			for(var i = 0; i < renderOptionParamsArray.length; i++) {
				$("#thumbs").append('<div id="' + i + '"></div>');
				$("#" + i).css("background-image", renderOptionsImage);
				$("#" + i).css('background-position', backgroundPosition[i]);
				$("#" + i).click(function(event){
					//alert(this.text + " " + "uploadedFile: " + uploadedFile + " selectedEffect: " + selectedEffect);
					//alert(event.target.id);
					render(event.target.id);
				});
			}
			//$("#thumbImageSample").attr({ src: renderOptionsGrid });
			showThumbs();
		},
		error: function(data, status, e)
		{
			alert(e);
		}
	});
	return false;
}

/*
 * Render image.
 */
function render(optionID)
{
	selectedRenderOption = parseInt(optionID); 
	renderOption = $.toJSON( renderOptionParamsArray[selectedRenderOption] );
	//console.log(renderOption);
	$.ajax({
		type: 'POST',
		url: 'cgi-bin/AviaryFxExample.py?q=render',
		dataType: 'json',
		data: ({ filterid: selectedEffect, filepath: uploadedFile, renderParameters: renderOption }),
		success: function(data, status)
		{
			//alert(data.url);
			renderedImage = data.url;
			$("#imageArea").attr({ src: data.url });
		},
		error: function(data, status, e)
		{
			alert(e);
		}
	});
	return false;
}

/*
 * Show/hide divs
 */
function showLoader()
{
	$("#loader").show();
}

function hideLoader()
{
	$("#loader").hide();
}

function hideUploadForm()
{
	$("#uploadForm").hide();
}

function showEffectOptions()
{
	$("#effectOptions").show();
}

function showThumbs()
{
	$("#thumbs").show();
}
