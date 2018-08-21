module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    postcss: {
      options: {
        processors: [
          require('postcss-import'),
          require('autoprefixer'),
          require('postcss-custom-media'),
          require('postcss-mixins'),
          require('postcss-custom-properties'),
          require('postcss-calc'),
          require('postcss-nesting'),
          require('postcss-color-function'),
          require('postcss-clean')
        ]
      },
      dist: {
        src: 'ckanext/lacounts/src/css/theme.css',
        dest: 'ckanext/lacounts/fanstatic/theme.css'
      }
    },

    uglify: {
      options: {
        mangle: false
      },
      my_target: {
        files: {
          'ckanext/lacounts/fanstatic/theme.js': ['ckanext/lacounts/src/js/main.js']
        }
      }
    },

    watch: {
      css: {
        files: 'ckanext/lacounts/src/css/*.css',
        tasks: ['postcss']
      },
      js: {
        files: 'ckanext/lacounts/src/js/*.js',
        tasks: ['uglify']
      }
    }

  });

  // Load the plugins
  grunt.loadNpmTasks('grunt-postcss');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  grunt.registerTask('default',['watch']);

};
