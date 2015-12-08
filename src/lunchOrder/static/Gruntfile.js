module.exports = function(grunt) {

	grunt.initConfig({
		pkg : grunt.file.readJSON('package.json'),
		dirs: {
		    js:{
		    	base: 'js/base',
		    	component: 'js/component'
		    }
		 },
		// 合并
		concat : {
			js_base:{
				options : {
					separator : ';'
				},
				src : ['<%= dirs.js.base %>/js_extension.js','<%= dirs.js.base %>/json2.js','<%= dirs.js.base %>/jquery_extend.js',
				'<%= dirs.js.base %>/ZeroClipboard.js','<%= dirs.js.base %>/jquery.dotdotdot.js'
				],
				dest : 'dist/js/base.js'
			},
			js_component : {
				options : {
					separator : ';'
				},				
				src : ['<%= dirs.js.component %>/draggable.js','<%= dirs.js.component %>/calendar.js','<%= dirs.js.component %>/droppable.js',
				'<%= dirs.js.component %>/resizable.js','<%= dirs.js.component %>/linkbutton.js','<%= dirs.js.component %>/panel.js',
				'<%= dirs.js.component %>/window.js','<%= dirs.js.component %>/dialog.js','<%= dirs.js.component %>/messager.js',
				'<%= dirs.js.component %>/form.js','<%= dirs.js.component %>/numberbox.js','<%= dirs.js.component %>/validatebox.js',
				'<%= dirs.js.component %>/combo.js','<%= dirs.js.component %>/combobox.js','<%= dirs.js.component %>/datebox.js',
				'<%= dirs.js.component %>/datetimebox.js','<%= dirs.js.component %>/parser.js','<%= dirs.js.component %>/messagelabel.js',
				'<%= dirs.js.component %>/tooltip.js','<%= dirs.js.component %>/placeholder.js','<%= dirs.js.component %>/spinner.js',
				'<%= dirs.js.component %>/numberspinner.js','<%= dirs.js.component %>/numberAdjust.js','<%= dirs.js.component %>/parabola.js',
				'<%= dirs.js.component %>/easyui-lang-zh_CN.js'
				],
				dest : 'dist/js/component.js'
			},
			css : {
				files : {
					'dist/css/component.css' : 'css/component/**.css'
				}

			}

		},
		cssmin : {
			minify : {
				expand : true,
				cwd : 'dist/css/',
				src : 'component.css',
				dest : 'dist/css/',
				ext : '.min.css'
			}
		},
		uglify : {
			options : {
				banner : '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
			},
			dist : {
				files : {
					'dist/js/base.min.js' : ['<%= concat.js_base.dest %>'],
					'dist/js/component.min.js' : ['<%= concat.js_component.dest %>']
				}
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.registerTask('default', ['concat','cssmin','uglify']);
};