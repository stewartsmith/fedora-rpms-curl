# Makefile for source rpm: curl
# $Id$
NAME := curl
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
