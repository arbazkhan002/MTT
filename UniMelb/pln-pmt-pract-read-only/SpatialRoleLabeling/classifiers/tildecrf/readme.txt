1.What this Programm is for
===========================
You can train a Conditional Random Fields and afterwards use the trained
modell either for classification or tagging of data.


2.Running
=============

The files lcrf.jar, log4j-1.2.9.jar and commons-cli-1.0.jar must be in the classpath.
The you can start lcrf using the following command line options:


java lcrf.Master [-n trainsteps] [-d null] [-z null] [--fold null] -m null [-h]
       [-y null] [-r null] [-l null] [-s null] [-x null] [-b null] [-w window
       size] [--validation atom2=filename] [--data atom3=filename] [--test
       atom2=filename] [--folds null] [--improvements null] [--train
       atom=filename]

    --fold          number of the fold used for testing in n-fold cross
                    validation
 -b                 File with Prolog backgroundknowledge
 -d                 maximum tree depth (default=7)
 -h,--help          show help
 -l                 minimum leaf size (default=10)
 -m,--mode          operation mode, possible values are: tagging,
                    classification, classificationoaa, classificationrr
 -n <trainsteps>    maximal number of training iterations of the CRF
                    (default 5)
 -r                 random seed (default 2342666)
 -s                 schemafile
 -w <window size>   window size (default 5)
 -x                 Sized of the subsample used for training the
                    regression model (default all)
 -y                 Increasement of the subsample size (default 100)
 -z                 Increase subsample size after n steps (default 2)

The trained models are not saved. You only see the result of classifying/tagging the
data after each training step.

3.Specification of the logger settings
======================================

The output is not printed to std, but it is printed using the log4j package.
To define the format of the output, you can modify the file logging.prop
For a detailed documentation see http://logging.apache.org/log4j/docs/


4.Format for Term Schemata
==========================

example:

  <schemata>
    <schema name="inputelement">
      <schematerm>a(X,Y)</schematerm>
      <substitutions variable="X">
        <numberconstant from="0" to="5"/>
      </substitutions>
    </schema>
    <schema name="outputelement">
      <schematerm>c(X)</schematerm>
      <substitutions variable="X">
        <numberconstant from="0" to="5"/>
        <entry>SUBST</entry>
      </substitutions>
    </schema>
  </schemata>

5.Format for Background Knowledge
=================================
You can specify background knowledge in a Prolog style.
Every predicate you want to be used as feature has to be in the 
format pred/1 and must be declared.
Internally, we use XProlog so don't expect all nifty prolog things
working.

( http://www.iro.umontreal.ca/~vaucher/XProlog/ )

example:

  <backgroundknowledge>
    <prolog>
      sameAsNext(N) :- sequence(N,he(X)), N2 is N+1, sequence(N2,he(Y)).
      sameAsNext(N) :- sequence(N,st(X)), N2 is N+1, sequence(N2,st(Y)).
      sameAsLast(N) :- N2 is N-1, sameAsNext(N2).
      inBlock(N)    :- sameAsNext(N), sameAsLast(N).
    </prolog>
    <feature name="sameAsNext"/>
    <feature name="sameAsLast"/>
    <feature name="inBlock"/>
  </backgroundknowledge>


6.Format of Data Files
======================

6.1 Classification Data
=======================
 example:
 
 <sequences>
 <sequence>
  <atom>strand(' SA',null,medium)</atom>
  <atom>strand(' SA',plus,medium)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SA',plus,medium)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SA',plus,short)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SA',plus,short)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SA',plus,medium)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SA',plus,short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SA',plus,short)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>strand(' SA',plus,medium)</atom>
  <atom>helix(h(right,alpha),short)</atom>
 </sequence>
 <sequence>
  <atom>strand(' SB',null,medium)</atom>
  <atom>strand(' SB',plus,medium)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SB',plus,medium)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SB',plus,short)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SB',plus,short)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SB',plus,medium)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>strand(' SB',plus,short)</atom>
  <atom>helix(h(right,alpha),long)</atom>
  <atom>helix(h(right,alpha),medium)</atom>
  <atom>strand(' SB',plus,short)</atom>
  <atom>helix(h(right,alpha),short)</atom>
  <atom>strand(' SB',plus,medium)</atom>
  <atom>helix(h(right,alpha),short)</atom>
 </sequence>
 </sequences>

6.2 Tagging Data
================

  example:
  
  <data>
  <classatoms>
    <atom>city(a)</atom>
    <atom>city(b)</atom>
    <atom>city(c)</atom>
    <atom>city(d)</atom>
  </classatoms>
  <sequence>
    <input>
      <entry>act(3,normal)</entry>
      <entry>act(3,fast)</entry>
    </input>
    <output>
      <entry>city(a)</entry>
      <entry>city(b)</entry>
    </output>
  </sequence>
    <sequence>
    <input>
      <entry>act(2,normal)</entry>
      <entry>act(2,fast)</entry>
    </input>
    <output>
      <entry>city(c)</entry>
      <entry>city(c)</entry>
    </output>
  </sequence>
  </data> 