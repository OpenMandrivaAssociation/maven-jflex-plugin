Name:           maven-jflex-plugin
Version:        1.4.3
Release:        6
Summary:        Maven JFlex Plugin

Group:          Development/Java
License:        GPLv3+
URL:            http://jflex.sourceforge.net/maven-jflex-plugin/
# Created by
# svn export http://jflex.svn.sourceforge.net/svnroot/jflex/tags/release_1_4_3/maven-jflex-plugin maven-jflex-plugin-1.4.3
# tar cjf maven-jflex-plugin-1.4.3.tar.bz2 maven-jflex-plugin-1.4.3/
Source0:        maven-jflex-plugin-1.4.3.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: jflex
BuildRequires: apache-commons-io
BuildRequires: maven2
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-testing-harness
Requires: jflex
Requires: apache-commons-io
Requires: maven2

%description
This is a Maven 2 plugin to generate a parser in Java code from
a Lexer definition, using Jflex.de.


%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q 

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap de.jflex %{name} %{version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

