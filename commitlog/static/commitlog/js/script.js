$(document).ready( function(){
	// initialize from history
	//http://tkyk.github.com/jquery-history-plugin/#demos
	function loadContent(hash) {
	    if(hash != "") {
	        //pages.new_page( hash +".html" );
	    } else {
	    	
	    	
		}
	}
	// initialize pages
	var pages = new PageManager($("#pages"));
	var tabs = new TabManager($("ul.tabs"), pages);
	var pagae1 = $(".page").html();
	$(".page").remove();
	pages.new_page( document.location.href, pagae1 );
	console.log(pages)
	// give current page id
	//$(".page").attr("id", pages.mk_page_id( document.location.href ) );
	tabs.mk_tab( document.location.href , $(".page h2").html() );
	//$.history.init(loadContent);
	// initialize tabs

	// ----------------- FILES --------------------
	$("#toogle_files").click( function(event){
		event.preventDefault();
		$(this).removeClass("open").addClass("closed");
		$('#tree').toggle("fast");
	})

	// ----------------- NEW FILE --------------------
	$("#create_new_file").click( function(){
		var loc = document.getElementById("cur_path").value + "/" +
			document.getElementById("new_file_name").value;
		document.location = loc;
	})

	// ----------------- PAGES --------------------
	$('#content').delegate('a.ajax', 'click', function(event) {
		event.preventDefault();
		var self = this;
		if (this.rel == "#pages") {
			// if its the same page do nothing
			if ( this.href != pages.current) {
				// hide current page
				pages.hide_current();
				//show if page is already loaded
				if ( pages.pages[this.href] ){
					tabs.activate_tab(this.href);
					pages.show_page(this.href);
				//creat new page
				} else { 
					var self = this;
					$.get(this.href, function(data) {
						pages.new_page(self.href, data.html );
					  	var tab_text = $(data.html).find("h1").text().replace('"', "");
					  	tabs.mk_tab(self.href, tab_text);
					}, "json")
				}				
			}
		}else {
			get_page(this.href, this.rel)
		}
		return false;
	});

	// ----------------- CONSOLE --------------------
	$("#console h4").click( function(){
		$("#console .content").toggle()
	})
	$("#console").draggable(function() {
	  helper: "original" 
	});

})

function prev_next( obj, current ) {
	// gets previous and next on both sides of current
	var prev_next = {"prev":null, "next":null};
	var var_prev = null;
	for (var key in obj){
		if (hasOwnProperty.call(obj, key)){
			if ( prev_next.prev ) {
				prev_next.next =  key;
				return prev_next
			}
			if ( key == current ) {
				prev_next.prev = var_prev;
			}
			var_prev = key;
		}

	}
}

function get_page(url, rel){
	var rel = rel;
	var url = url; 
	$.get(url, function(data) {
		$(rel).html( data.html  )
	}, "json")
}

function TabManager( tab_container, pages ){
	this.tab_container = tab_container;
	this.pages = pages;
	this.current = previous = next = "";
	var self = this;

	tab_container.delegate("li", 'click', function(event){
		event.preventDefault();
		self.deactivate_tabs();
		var tab = $(this);
		tab.addClass("active");
		self.pages.hide_current();
		self.pages.show_page(tab.find("a.tab").attr("href"));
		return false;
	});

	this.get_tabs = function() {
		
	}
	this.mk_tab = function( url, title ){
		this.deactivate_tabs();
		return this.tab_container.append("<li class='active' ><a href='#' class='close' title='close tab' >x</a><a href='" + url + "' title='"+ title +"' class='tab' >" + title + "</a></li>")
	}
	this.rm_tab = function( url ){
		var tab_to_remove = this.get_tab_by_url( url ).parent()
		tab_to_remove.remove();
		prev_next = prev_next( this.pages.pages, url )
		
		if (prev_next.prev) {
			this.pages.show_page(prev_next.prev);
		}
		
	}
	this.deactivate_tabs = function( ){
		this.tab_container.find("li").removeClass("active");
	}
	this.get_tab_by_url = function( url ){
		return this.tab_container.find("a.[href='" + url +"']")
	}
	this.activate_tab = function( url ){
		this.deactivate_tabs();
		this.get_tab_by_url( url ).parent().addClass("active");
	}
}


function PageManager( page_container, options ){

	this.current = "";
	this.page_container = page_container;
	this.pages = {};
	this.transition = false;
	this.new_page = function( url, data ){
		var id = this.mk_page_id( url );
		this.pages[url] = id;
		this.set_current( url );
        //url = url.replace(/^.*#/, '');
        //$.history.load(url);
		return this.page_container.append("<div class='page' id='" + id + "' >" + data + "</div>");
	}
	this.rm_page = function( url ){
		$("#"+this.get_page_id(url)).remove();
		delete this.pages[url]
	}
	this.mk_page_id = function( url ){
		return url.replace(/\//g, "_").replace(/\./g, "").replace(/:/g, "")
	}
	this.set_current = function( url ){
		this.current = url;
	}
	this.get_page_id = function( url ){
		return this.pages[url]
	}
	this.get_current_id = function( ){
		return this.pages[ this.current ]
	}
	this.get_page = function( url ){
		return $("#"+this.pages[ url ])
	}
	this.get_current = function( ){
		return $("#"+this.pages[ this.current ])
	}
	this.hide_current = function( ){
		var page = this.get_current( );
		this.transition = true;
		var self = this;
		var url = url;
		return page.hide('slide', {direction: 'left'}, 700, function(){
			self.transition = false;
		});
	}
	this.show_page = function( url ){
		var page = this.get_page( url );
		this.set_current( url );
		page.show();
	}
}